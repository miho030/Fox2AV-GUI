################################################################################
##
## BY: github.com/miho030
## PROJECT MADE WITH: Qt Designer and PySide6
## V: 1.1.1
##
"""
pyrcc5 -o resources_rc.py resources.qrc
"""
################################################################################

import os, sys, re, time, json, warnings, shutil
import threading, queue, configparser, logging
from datetime import datetime
from typing import Any, List, Tuple
from json import JSONDecodeError

from PySide6 import QtCore
from PySide6.QtGui import (QAction, QIcon, QDesktopServices)
from PySide6.QtWidgets import *

## ==> for req scan
from PySide6.QtCore import Signal, QObject, QThread, Slot
from PySide6.QtCore import Qt, QEvent

## ==> GUI FILE
from ui_main import Ui_Fox2Av

## ==> import Fox2AV core
import Fox2Av.Foxcore.PlugInEngine.Signature as sig2
from Fox2Av.Foxcore.singletone import infection_registry

## ==> import Fox2AV preset loader modules
import presets as fox2av_presets

## ==> import Fox2AV UI/UX modules
from Fox2UI.toast_popup import show_detection_toast

## ==> for sound play
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl


## ==> GLOBAL SETTINGS
DB_PATH = "./Fox2Av/Foxdb/main.hdb"
memory = 1024 * 100  # 102400

log_dir = os.path.abspath("./Common/logs/")
quarantine_dir = os.path.abspath("./Common/Quarantine/")
qurantine_sector_dir = os.path.abspath("./Common/Quarantine/Sectors/")
settings_dir = os.path.abspath("./Common/Settings/")
Fox2AV_settings = settings_dir + "/Fox2AV_settings.ini"

""" Pre-load Fox2av presets """
fox2av_presets.fox2av_preset_maker()
fox2av_presets.fox2av_startup_set_manager()

""" global handlers """
inicfg = configparser.ConfigParser()
_settings_loaded = False # guard flag

""" sound play """
_active_sounds: list[QSoundEffect] = []

# effect 이름, 파일 경로 맵
_SOUND_PATHS = {
    "detected":    "./Sounds/detected.wav",
    "alert":       "./Sounds/alert.wav",
    "deleted":     "./Sounds/deleted.wav",
    "error":       "./Sounds/error.wav",
    "error2":      "./Sounds/error2.wav",
    "clicked":     "./Sounds/clicked.wav",
    "not_work":    "./Sounds/not_work.wav",
    "popup_open":  "./Sounds/popup.open.wav",
}

def check_set_file():
    global _settings_loaded
    if _settings_loaded:
        return

    if not os.path.isfile(Fox2AV_settings):
        logging.warning(f"{Fox2AV_settings} not found, apply the default settings.")
        try:
            fox2av_presets.reRoll_to_default_set()
            logging.info("Default settings successfully applied.")
        except Exception as e:
            logging.critical(f"Error applying preferences: {e}")
    else:
        logging.info(f"{Fox2AV_settings} successfully loaded.")

    _settings_loaded = True

def update_set_data(section: str, keyValue : str, newData :str):
    if not os.path.isfile(Fox2AV_settings):
        logging.critical(f"Failed to change settings {Fox2AV_settings} not found, apply the default settings.")
        check_set_file()
    inicfg.read(Fox2AV_settings, encoding="utf-8")

    if not inicfg.has_section(section):
        logging.critical(f"{section} not found in {Fox2AV_settings}. Abort change process.")
        return False

    if not inicfg.has_option(section, keyValue):
        logging.error(f"{keyValue} not found in {section} section. No change required.")
        return False

    old_value = inicfg.get(section, keyValue)
    if old_value == newData:
        logging.info(f"{section} value {keyValue} already {newData}. No change required.")
        return True
    inicfg.set(section, keyValue, newData)
    try:
        with open(Fox2AV_settings, "w", encoding="utf-8") as fp:
            inicfg.write(fp)
        logging.info(f"[{section}] {keyValue} successfully updated to {newData}.")
        return True
    except Exception as e:
        logging.error(f"Fox2AV settings update failed: {e}")
        return False


def get_set_data(indexValue: str, keyValue: str):
    try:
        inicfg.read(Fox2AV_settings, encoding="utf-8")
        return inicfg.get(indexValue, keyValue, fallback="N/A")
    except IOError as e:
        logging.warning(f"Failed to load Fox2AV setting file. {e} -- running autochecker..")
        check_set_file()


def newest_scan_timestamp():
    SCAN_RE = re.compile(r"^(?:tarScan|entScan)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})$")

    latest_dt = None
    latest_ts = None
    for date_dir in os.listdir(log_dir):
        scan_root = os.path.join(log_dir, date_dir, "scanLogs")
        if not os.path.isdir(scan_root):
            continue

        for scan_dir in os.listdir(scan_root):
            m = SCAN_RE.match(scan_dir)
            if not m:
                continue

            ts_str = m.group(1)
            try:
                ts_dt = datetime.strptime(ts_str, "%Y-%m-%d_%H-%M-%S")
            except ValueError:
                continue

            if latest_dt is None or ts_dt > latest_dt:
                latest_dt, latest_ts = ts_dt, ts_str
    update_set_data("ScanHistory", "last_scan_date", latest_ts)
newest_scan_timestamp()


""" Pre-load malware database """
########################################################################
def DB_Pattern():
    File_Hash_List, File_Size_List, File_Name_List = [], [], []
    Malware_SignatureDB_version = None

    with open(DB_PATH, "r", encoding="utf-8") as fdb:
        for line in fdb:
            decoded = line.strip()
            if ':' not in decoded:
                Malware_SignatureDB_version = decoded
                continue

            try:
                hash_str, size_str, name_str = decoded.split(':', 2)
                File_Hash_List.append(hash_str)
                File_Size_List.append(int(size_str))
                File_Name_List.append(name_str)
            except ValueError:
                logging.warning(f"{decoded!r} is not a valid pattern entry")
                continue

    update_set_data("Update", "last_update_dbver",
                    Malware_SignatureDB_version)  # renew db version data to fox2av ini file
    return (
        Malware_SignatureDB_version,
        File_Hash_List, File_Size_List, File_Name_List
    )
Malware_SignatureDB_version, File_Hash_List, File_Size_List, File_Name_List = DB_Pattern()  # Load the patterns into memory at startup



class req_Scan(QObject):
    finished = Signal()
    progress = Signal(int)
    update_label = Signal(str)
    update_status = Signal(str)

    def __init__(self, scan_function, drive_queue, file_hash_list, file_name_list, scanlogger=None):
        super().__init__()
        ##>> for scan process
        self._stop_event = threading.Event()
        self.scan_function = scan_function
        self.drive_queue = drive_queue
        self.file_hash_list = file_hash_list
        self.file_name_list = file_name_list
        self.scanlogger = scanlogger

        ##>> for targeted scan functions
        self.targeted_dir_name = None

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            self.scan_function(
                self.drive_queue,
                self.progress.emit,
                self.update_label.emit,
                self.update_status.emit,
                self._stop_event,
                self.file_hash_list,
                self.file_name_list,
                logger=self.scanlogger
            )
        except Exception as e:
            if self.scanlogger:
                self.scanlogger.exception("Exception occurred during scanning process")
            else:
                logging.exception("Exception occurred during scanning process")
            logging.debug(f"Exception in run method: {e}")
        finally:
            if self.scanlogger:
                self.scanlogger.debug(f"Sending 'finished' siganl to scan engine...")
            logging.debug(f"Senging Emitting finshed signal to scan engine..")
            self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Fox2Av()
        self.ui.setupUi(self)

        """ Fox2Av Startup Func """
        ########################################################################
        self.setup_logging()
        logging.info("Fox2AV-GUI Application started")
        logging.info(f"✔ Loaded total {len(File_Hash_List)} patterns | DB version: {Malware_SignatureDB_version}")

        # 모니터링 페이지 초기화 메서드 호출
        self.ui.mon_db_ver_info_data.setText(Malware_SignatureDB_version)

        ### Qurantine side
        # secure qurantine sector
        self.secure_quarantine_sector(qurantine_sector_dir)
        self.qurantine_sector_dir = qurantine_sector_dir

        """ Windows settings """
        ########################################################################
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.oldPos = self.pos()

        """ GUI App SystemTry Settings """
        ########################################################################
        self.tray_icon = QSystemTrayIcon(self)  # 시스템 트레이 아이콘 생성
        self.tray_icon.setIcon(QIcon("images/logo_small.png"))

        tray_menu = QMenu()  # 트레이 아이콘 메뉴 생성

        # add quick scan
        quick_scan = QAction("Quick Scan", self)
        tray_menu.addAction(quick_scan)

        # turn off auto virus scan
        off_auto_virusScan = QAction("Turn off Auto Scan", self)
        tray_menu.addAction(off_auto_virusScan)

        # turn off real-time protection
        off_rt_protection = QAction("Turn off Real-Time Protection", self)
        tray_menu.addAction(off_rt_protection)

        # add seperator
        tray_menu.addSeparator()

        # open fox2av
        restore_action = QAction("Open Fox2AV", self)
        restore_action.triggered.connect(self.show)
        tray_menu.addAction(restore_action)

        # quit fox2av
        quit_action = QAction("Quit Fox2AV", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.show()

        """ Fox2Av Main Frame Settings """
        ########################################################################
        ## ==> Fox2AV author page redirect
        self.ui.fox2av_Name_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.open_homepage()
            )
        )
        self.ui.fox2av_sub_Author_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.open_github()
            )
        )

        ## ==>  Main Init
        self.ui.sub_btn_close.installEventFilter(self)
        self.ui.sub_btn_close.clicked.connect(self.close)
        self.ui.sub_btn_minimalized.clicked.connect(self.showMinimized)

        ## ==> initialize stackedWidget pages
        self.ui.stackedWidget.setCurrentWidget(self.ui.monitoring)
        self.ui.SubFrame_Main_stackedWidget.setCurrentWidget(self.ui.SubFrame_Main)

        """ subFrame_Main stackedWidget btn animation """
        ########################################################################
        ##>> for btn animations, 버튼 그룹 생성
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.buttons = [self.ui.btn_Monitoring, self.ui.btn_Scan, self.ui.btn_report, self.ui.btn_Quarantine]

        for idx, button in enumerate(self.buttons):
            button.setCheckable(True)
            self.button_group.addButton(button, idx)
            button.clicked.connect(self.create_button_click_handler(idx))

        self.buttons[0].setChecked(True) # 첫 번째 버튼을 기본 선택으로 설정
        self.update_button_styles(0)


        """ Fox2Av Settings StackedWidget settings """
        ########################################################################
        self.ui.sub_btn_settings.clicked.connect(self.show_settings)
        self.ui.setting_to_main_btn.clicked.connect(self.show_main)

        """ Fox2Av Settings SubTabTree settings """
        self.ui.Settings_General_btn.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_General)
            )
        )
        self.ui.Settings_Update_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_General_Update)
            )
        )
        self.ui.Settings_Notification_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_General_Notification)
            )
        )
        self.ui.Settings_Privacy_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_General_Privacy)
            )
        )
        self.ui.Settings_Scan_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_Scan)
            )
        )
        self.ui.Settings_RT_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_Scan_RT)
            )
        )
        self.ui.Settings_Exclusion_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_Scan_Exclusions)
            )
        )
        self.ui.Settings_Advanced_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_Scan_Advanced)
            )
        )
        self.ui.Settings_Quarantine_btn.clicked.connect(
            lambda : (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_Quarantine)
            )
        )


        """ Fox2Av PAGES Settings """
        ########################################################################
        ## ==> PAGE monitoring
        self.ui.btn_Monitoring.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui.monitoring)
            )
        )
        # get data from ini file
        last_fox2av_ver = get_set_data("Update", "latest_fox2av_version")
        last_db_ver = get_set_data("Update", "last_update_dbVer")
        auto_scan_value = get_set_data("Scan", "auto_virus_scan")
        real_time_scan_value = get_set_data("General", "real_time_protection")
        recent_scan_date = get_set_data("ScanHistory", "last_scan_date")

        # set dashboard data from ini file
        self.ui.fox2av_sub_sfName.setText("Fox2AV " + last_fox2av_ver + " -alpa")
        self.ui.mon_db_ver_info_data.setText(last_db_ver)
        self.ui.mon_recentScanDate_data.setText(recent_scan_date)
        self.ui.mon_autoScan_status_data.setText(auto_scan_value)
        self.ui.mon_rt_status_data.setText(real_time_scan_value)

        ## ==> PAGE scan
        self.ui.btn_Scan.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui.scan)
                )
            )
        ## ==> PAGE scan_Main
        self.ui.tar_btn_Scan.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_set_targeted_page)
            )
        )
        self.ui.ent_btn_Scan.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_entire_page),
                self.ui.ent_btn_Scan.clicked.connect(self.start_ent_scan)
            )
        )
        self.ui.cus_btn_Scan.clicked.connect(
            lambda: (
                self.play_sound_effect("not_work"),
                self.call_info_preparing()
            )
        )

        ## ==> PAGE _scan -> set_targeted_scan page
        self.ui._scan_set_tar_btn_openFolder.clicked.connect(self._scan_tar_open_dir)
        self.ui._scan_set_tar_btn_scannow.clicked.connect(
            lambda:
            self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_targeted_page)
        )
        self.ui._scan_set_tar_btn_scannow.clicked.connect(self.start_tar_scan)
        self.ui._scan_set_tar_btn_back_to_ScanMain.clicked.connect(
            lambda:
            self.ui.Scan_stackedWidget.setCurrentWidget(self.ui.Scan_Main)
        )

        # TreeWidget 헤더 숨기기
        self.ui._scan_set_tar_driveTree.setHeaderHidden(True)

        ## ==> PAGE _scan -> targeted_scan page
        self.ui._scan_tar_btn_back_to_ScanMain.clicked.connect(
            lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_set_targeted_page))
        self.ui._scan_tar_btn_stop_scan.clicked.connect(self.stop_tar_scan)

        ## ==> PAGE _scan -> entire_scan page
        self.ui._scan_ent_btn_back_to_ScanMain.clicked.connect(
            lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui.Scan_Main))
        self.ui._scan_ent_btn_stop_scan.clicked.connect(self.stop_ent_scan)

        ## ==> scan - custom_scan page
        ###


        ## ==> PAGE report
        self.ui.btn_report.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui.report)
            )
        )
        self.ui.log_report_table_widget.setColumnCount(4)
        self.ui.log_report_table_widget.setHorizontalHeaderLabels(
            ["Log creation date", "Log type", "File Name", "Log file path"])
        self.ui.threat_report_table_widget.setColumnCount(7)
        self.ui.threat_report_table_widget.setHorizontalHeaderLabels(
            ["Detection time", "Risk Level", "File name", "Threat name",  "Threat Path" "Action Status", "md5 hash", "Scan engine"])


        ## ==> PAGE Qurantine
        self.ui.btn_Quarantine.clicked.connect(
            lambda: (
                self.play_sound_effect("clicked"),
                self.ui.stackedWidget.setCurrentWidget(self.ui.Quarantine)
            )
        )
        self.ui.qurantine_refresh_btn.clicked.connect(
            lambda: (
                self.play_sound_effect("deleted"),
                self.make_quarantine_list(self.qurantine_sector_dir)
            )
        )
        self.ui.quarantine_table_widget.setColumnCount(4)
        self.ui.quarantine_table_widget.setHorizontalHeaderLabels(
            ["Quarantined time", "Threat name", "File name", "Action status", "Threat Path"])
        self.ui.qurantine_delete_btn.clicked.connect(
            lambda: (
                self.play_sound_effect("error2"),
                self.on_Quarantine_remove_clicked()
            )
        )


        # ==> PAGE Report, Quarantine 유저 친화 설정
        table_widgets = [
            self.ui.log_report_table_widget,
            self.ui.threat_report_table_widget,
            self.ui.quarantine_table_widget
        ]
        for table_widget in table_widgets:
            header = table_widget.horizontalHeader()

            for i in range(table_widget.columnCount()): # 모든 컬럼에 대해 자동 크기 조정 설정
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

            header.setStretchLastSection(False)
            header.setSectionsMovable(True)  # 사용자가 컬럼을 이동 및 크기 조정가능하도록
            table_widget.setSizePolicy(table_widget.sizePolicy().horizontalPolicy(),
                                       table_widget.sizePolicy().verticalPolicy())



        """ Fox2AV UI/UX IMPROVE FUNCTIONS """
        ########################################################################
        def apply_corner_button_style(table_widget):
            for child in table_widget.children():
                if child.metaObject().className() == "QTableCornerButton":
                    child.setStyleSheet("QTableCornerButton::section {background-color: transparent;border: none;}")
                    break

        # TableWidget Corner button 비활성화 및 색상 처리
        apply_corner_button_style(self.ui.log_report_table_widget)
        apply_corner_button_style(self.ui.quarantine_table_widget)
        apply_corner_button_style(self.ui.threat_report_table_widget)

        """ Fox2AV LOG UI INIT FUNCTIONS """
        ########################################################################
        # log_report 관련 기능 구현
        self.make_log_list(log_dir)
        log_report_layout = QVBoxLayout()
        log_report_layout.addWidget(self.ui.log_report_table_widget)
        self.setLayout(log_report_layout)

        # Thread_report 관련 기능 구현
        self.make_threat_report(log_dir)
        threat_report_layout = QVBoxLayout()
        threat_report_layout.addWidget(self.ui.threat_report_table_widget)
        self.setLayout(threat_report_layout)

        # Quarantine_report 관련 기능 구현
        self.make_quarantine_list(qurantine_sector_dir)
        quarantine_layout = QVBoxLayout()
        quarantine_layout.addWidget(self.ui.quarantine_table_widget)
        self.setLayout(quarantine_layout)

        # 수평 헤더 (행,열 제목, 코너버튼) 배경색 변경
        self.ui.log_report_table_widget.horizontalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.log_report_table_widget.verticalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.threat_report_table_widget.horizontalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.threat_report_table_widget.verticalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.quarantine_table_widget.horizontalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.quarantine_table_widget.verticalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(32, 41, 64);}")

        """ Fox2AV FUNCTIONS """
        ########################################################################
        # 선택 바이러스 검사 기능의 드라이브 표시 및 출력, 선택 tree widget 생성 관련 코드
        drives = self._scan_tar_get_drives()

        for drive in drives:
            item = QTreeWidgetItem(self.ui._scan_set_tar_driveTree)
            item.setText(0, drive)
            item.setCheckState(0, Qt.Unchecked)  # 체크박스를 추가

        ## SHOW ==> MAIN WINDOW ==> END
        ########################################################################
        self.show()

    """ Open Fox2AV homepage """
    def open_homepage(self):
        url = QUrl("https://github.com/miho030/Fox2AV-GUI")
        QDesktopServices.openUrl(url)
    def open_github(self):
        url = QUrl("https://github.com/miho030/")
        QDesktopServices.openUrl(url)

    """ Fox2AV Setting Swap FUNCTIONS """
    def show_settings(self):
        self.play_sound_effect("clicked")
        self.ui.stackedWidget.setCurrentWidget(self.ui._Settings_General)
        self.ui.SubFrame_Main_stackedWidget.setCurrentWidget(self.ui.SubFrame_Settings)

    def show_main(self):
        self.play_sound_effect("deleted")
        self.ui.stackedWidget.setCurrentWidget(self.ui.monitoring)
        self.ui.SubFrame_Main_stackedWidget.setCurrentWidget(self.ui.SubFrame_Main)


    """ Fox2AV Startup Funcs """
    def setup_logging(self):
        """ global 로그 파일 기록 관련 로거 및 핸들러 설정 """
        # 현재 날짜, 시간 기반으로 파일 및 폴더 생성
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        date_folder_path = os.path.join(log_dir, current_date)  # 날짜별 로그 디렉터리
        os.makedirs(date_folder_path, exist_ok=True)
        os.makedirs(os.path.join(date_folder_path, "scanLogs/"), exist_ok=True)

        global_log_file_name = f"global_{current_date}.log"
        global_log_file_path = os.path.join(date_folder_path, global_log_file_name)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # 로그 메시지 형식 설정
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        global_file_handler = logging.FileHandler(global_log_file_path, encoding="utf-8")  # 글로벌 로깅 핸들러
        global_file_handler.setFormatter(formatter)
        logger.addHandler(global_file_handler)

        global_console_handler = logging.StreamHandler()  # 콘솔 핸들러 설정 (디버그 - 터미널에 출력)
        global_console_handler.setFormatter(formatter)
        logger.addHandler(global_console_handler)

        logging.info(f"Global Log file created: {global_log_file_path}")

        self.scanlogger = logging.getLogger("scanlogger")
        self.scanlogger.setLevel(logging.DEBUG)

        if len(self.scanlogger.handlers) > 0:  # 기존 핸들러 제거 (중복 로그 방지)
            for handler in self.scanlogger.handlers[:]:
                self.scanlogger.removeHandler(handler)
                handler.close()

    def set_scan_log_file(self, scanLogDir, scanLogFileName, scan_type):
        """ scan_type: entScan 또는 tarScan을 지정하여 해당 로그 파일을 설정 """
        log_file_name = scanLogFileName
        scan_log_file = os.path.join(scanLogDir, log_file_name)

        if len(self.scanlogger.handlers) > 0:  # 기존 핸들러 제거 (중복 로그 방지)
            for handler in self.scanlogger.handlers[:]:
                self.scanlogger.removeHandler(handler)
                handler.close()

        self.scanlogger.setLevel(logging.DEBUG)

        # 로그 메시지 형식 설정
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(scan_log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.scanlogger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.scanlogger.addHandler(console_handler)

        # 글로벌 로거로 로그 전파 방지
        self.scanlogger.propagate = False
        self.scanlogger.info(f"Scan Log file created: {scan_log_file}")


    """ Fox2AV INIT FUNCTIONS """
    ########################################################################
    # Fox2AV APP SystemTray
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        fox2Av_icon = QIcon("images/logo_small.png")
        self.tray_icon.showMessage(
            "Fox2AV",
            "Fox2AV is running in the system tray.",
            fox2Av_icon,
            2000
        )

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()
            self.raise_()
            self.activateWindow()

    # Scan > Targeted Scan > Search and list system drives
    def _scan_tar_get_drives(self):
        """ 윈도우 시스템에서 드라이브 목록 가져오기 """
        drives = []
        for drive in range(ord('A'), ord('Z') + 1):
            drive_letter = f"{chr(drive)}:\\"
            if os.path.exists(drive_letter):
                drives.append(drive_letter)
        return drives

    # Scan > Targeted Scan > open other folder
    def _scan_tar_open_dir(self):
        self.targeted_dir_name = QFileDialog.getExistingDirectory(self, 'Select folder', '')
        return self.targeted_dir_name

    # Scan > Custom Scan > Scano now button
    def call_info_preparing(self):
        QMessageBox.information(self, "Information", "We are preparing this function!\nSee you soon XD")

    def call_info_cancled(self):
        QMessageBox.information(self, "Information", "Scanning stopped.")


    """ Fox2AV ANIMATION FUNCTIONS """
    ########################################################################
    def create_button_click_handler(self, index):
        def handler():
            self.ui.stackedWidget.setCurrentIndex(index)
            self.update_button_styles(index)
        return handler

    def update_button_styles(self, clicked_index):
        """ 종료 버튼 스타일 업데이트 기능 구현 (애니메이션)"""
        for idx, button in enumerate(self.buttons):
            if idx == clicked_index:
                button.setStyleSheet("background-color: rgb(32, 41, 64)")
            else:
                button.setStyleSheet("background-color: rgba(255, 255, 255, 0)")

    # Fox2AV APP -> for FrameLess windows
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Deprecated: self.oldPos = event.globalPos()
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Deprecated: delta = QPoint(event.globalPos() - self.oldPos)
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    # for Close Icon/Button Animation
    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter and source == self.ui.sub_btn_close:
            self.ui.sub_btn_close.setStyleSheet(
                "image: url(:/png/images/Universal/hightited_close.png);background-color: rgb(32, 41, 64, 0);")
        elif event.type() == QEvent.Leave and source == self.ui.sub_btn_close:
            self.ui.sub_btn_close.setStyleSheet(
                "image: url(:/png/images/Universal/close_negative.png);background-color: rgb(32, 41, 64, 0);")
        return super().eventFilter(source, event)

    # for sound play effects
    def play_sound_effect(self, effect: str, volume: float = 0.5):
        file_path = _SOUND_PATHS.get(effect)
        if not file_path: # 정의되지 않은 키면 재생하지 않음
            return

        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(file_path))
        sound.setVolume(volume)
        sound.play()
        _active_sounds.append(sound)
        sound.playingChanged.connect(
            lambda s=sound: (
                _active_sounds.remove(s)
                if not sound.isPlaying() and s in _active_sounds
                else None
            )
        )

    """ Fox2AV MAIN FUNCTIONS """
    ########################################################################
    @Slot(int)
    def tar_update_progress(self, value):
        self.ui._scan_tar_processbar.setValue(value)

    @Slot(str)
    def tar_update_status(self, text):
        self.ui._scan_tar_ScanStatus.setText(text)

    @Slot(str)
    def tar_update_label(self, text):
        self.ui._scan_tar_current_scanFile.setText(text)

    @Slot(int)
    def ent_update_progress(self, value):
        self.ui._scan_ent_processbar.setValue(value)

    @Slot(str)
    def ent_update_status(self, text):
        self.ui._scan_ent_ScanStatus.setText(text)

    @Slot(str)
    def ent_update_label(self, text):
        self.ui._scan_ent_current_scanFile.setText(text)

    @Slot()
    def on_tarScan_finished(self):
        infections = list(infection_registry.get_infections())
        infected_cnt = len(infections)

        self.play_sound_effect("detected")
        show_detection_toast(infected_cnt, infections, parent=self)
        self._afterScan_handler(infections, self._tar_current_scan_log_dir,self._tar_current_scan_datetime, "tarScan")

        self.ui._scan_tar_btn_back_to_ScanMain.setEnabled(True)
        self.scanlogger.info("[SCAN END] - Targeted system scan ended.")
        self.thread_tarScan.quit()

    @Slot()
    def on_entScan_finished(self):
        infections = list(infection_registry.get_infections())
        infected_cnt = len(infections)

        show_detection_toast(infected_cnt, infections, parent=self)
        self._afterScan_handler(infections, self._ent_current_scan_log_dir,self._ent_current_scan_datetime, "entScan")

        self.ui._scan_ent_btn_back_to_ScanMain.setEnabled(True)
        self.scanlogger.info("[SCAN START] - Entire system scan ended.")
        self.thread_entScan.quit()


    def _afterScan_handler(self, infection_list, scan_res_dir, scan_datetime, scan_type):
        """ 스캔 종료 후 감염 파일을 실행 불가능한 파일 형식(*.fxav)로 수정하고 격리소로 이동시킨다. """
        auto_secure_option = get_set_data("Quarantine", "auto_qurantine_option")
        is_secured = ""
        if auto_secure_option == 'false':
            is_secured = "ignored(not secured)"
        elif auto_secure_option == 'true':
            is_secured = "deactivated/quarantined"

            """ 탐지된 악성코드 파일 비활성화/격리/삭제 조치 시작 지점 """
            for dirs in infection_list:
                threat_file_name = dirs[1]
                threat_file_path = dirs[3]

                if os.path.exists(threat_file_path):
                    original_file_name = os.path.splitext(threat_file_name)[0]
                    secured_file_name = f"{original_file_name}.fxav"
                    secured_file_path = os.path.join(qurantine_sector_dir, secured_file_name)
                    if not os.path.exists(secured_file_path):
                        shutil.copy2(threat_file_path, secured_file_path) # 탐지된 악성코드 파일 비활성화 및 격리 구역으로 격리
                        logging.info("[SECURED] detected malware file '%s' has been secured at '%s'.", threat_file_path,
                                     secured_file_path)
                    os.remove(threat_file_path) # 탐지된 악성코드 파일 삭제 조치
                    logging.info(f"Malware file deleted: {threat_file_path}")
            """ 탐지된 악성코드 파일 비활성화/격리/삭제 조치 종료 지점 """


            # 격리된 파일 정보를 qurantined.dat 에 저장
            detectResList = []
            qurantine_log_dir = quarantine_dir + "/" + "qurantined.dat"

            for resDat in infection_list:
                detectResList.append({
                    "Detection time": resDat[0],
                    "Risk level": "High",
                    "Action": is_secured,
                    "Threat name": resDat[2],
                    "File name": resDat[1],
                    "Threat path": resDat[3],
                    "md5 hash": resDat[4],
                    "Scan engine": "Fox2AV-Sigv1/" + scan_type
                })
            os.makedirs(os.path.dirname(qurantine_log_dir), exist_ok=True)
            with open(qurantine_log_dir, "a", encoding="utf-8") as f:
                for entry in detectResList:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            # 검사 종료 후 threat report 관련 정보 저장
            detectResFile_dir = scan_res_dir + "/" + "detectRes.json"
            shutil.copy2(qurantine_log_dir, detectResFile_dir)

        """스캔 종료 후 감염 결과를 JSON 두 형태로 기록한다."""
        # 탐지된 악성코드 정보 저장
        detectInfoFile_dir = scan_res_dir + "/" + "detectInfo.json"
        with open(detectInfoFile_dir, "w", encoding='utf-8') as f:
            json.dump(infection_list, f, ensure_ascii=False, indent=4)



    def clean_up_scan(self, scan_handler, scan_thread):
        """ 스레드와 핸들러를 안전하게 종료하고 메모리에서 삭제하는 함수 """
        try:
            if scan_thread and scan_thread.isRunning(): # 스레드가 실행 중인 경우 안전하게 종료
                logging.info("Thread is running, attempting to quit...")
                scan_thread.quit()
                scan_thread.wait()

            if scan_handler: # 시그널 연결 해제 및 메모리 삭제
                if scan_handler.signalsBlocked():
                    scan_handler.blockSignals(False)

                try: # 시그널 연결 해제 (이미 해제된 경우를 대비해 예외 처리)
                    scan_handler.finished.disconnect()
                    scan_handler.progress.disconnect()
                    scan_handler.update_label.disconnect()
                    scan_handler.update_status.disconnect()
                except (TypeError, RuntimeError) as e:
                    logging.warning(f"Handler signal already disconnected: {e}")

                scan_handler.deleteLater()
                self.h_tarScan = None
                self.h_entScan = None

            if scan_thread:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=RuntimeWarning)
                        scan_thread.finished.disconnect()
                except (TypeError, RuntimeError, Exception) as e:
                    logging.warning(f"Failed to disconnect finished signal: {e}")

                scan_thread.deleteLater()
                self.thread_tarScan = None
                self.thread_entScan = None

            logging.info("Scan and thread cleanup completed safely.")

        except Exception as e:
            logging.error(f"Error during scan cleanup: {e}")



    def start_tar_scan(self):
        # 현재 날짜와 시간을 이용하여 로깅 및 결과 저장을 위한 scanLog 폴더 생성
        now = datetime.now()
        scanStartDate = now.strftime("%Y-%m-%d")
        scanStartTime = now.strftime("%H-%M-%S")

        self._tar_current_scan_datetime = f"{scanStartDate}_{scanStartTime}"
        seperated_log_name              = f"tarScan_{self._tar_current_scan_datetime}"
        scan_log_file                   = f"tarScan_{scanStartDate}_{scanStartTime}.log"

        self._tar_current_scan_log_dir  = os.path.join(log_dir, scanStartDate, "scanLogs", seperated_log_name) # 로그 파일 전체 경로 설정
        os.makedirs(os.path.join(self._tar_current_scan_log_dir), exist_ok=True)  # 스캔 결과별 폴더 생성


        checked_drive_list = []  # QTreeWidget에서 체크된 항목을 확인
        root = self.ui._scan_set_tar_driveTree.invisibleRootItem()
        child_count = root.childCount()

        for i in range(child_count):
            item = root.child(i)
            if item.checkState(0) == Qt.Checked:
                checked_drive_list.append(item.text(0))

        # QTreeWidget에서 체크된 항목도 없고, 사용자가 폴더도 선택하지 않은 경우 경고 메시지 출력
        if not checked_drive_list and self.targeted_dir_name is None:
            QMessageBox.warning(self, "Warning!", "Please select Scan directory path.")
            return

        if not (checked_drive_list == None) or (self.targeted_dir_name == None):
            drive_queue = queue.Queue()
            if checked_drive_list:
                for drive in checked_drive_list:
                    drive_queue.put(drive)
            else:
                drive_queue.put(self.targeted_dir_name)

            # Targeted Scan 로그 파일 설정
            self.set_scan_log_file(self._tar_current_scan_log_dir, scan_log_file, scan_type="tarScan")
            logging.info("* checking Fox2AV.Main Singletone system..." + "\n\t▶ infection_registry ID: %s\n",
                         id(infection_registry))

            self.h_tarScan = req_Scan(sig2.scan_targeted, drive_queue, File_Hash_List, File_Name_List,
                                      scanlogger=self.scanlogger)
            self.thread_tarScan = QThread()
            self.h_tarScan.moveToThread(self.thread_tarScan)

            self.h_tarScan.progress.connect(self.tar_update_progress)
            self.h_tarScan.update_label.connect(self.tar_update_label)
            self.h_tarScan.update_status.connect(self.tar_update_status)
            self.thread_tarScan.started.connect(self.h_tarScan.run)

            self.h_tarScan.finished.connect(self.on_tarScan_finished)
            self.scanlogger.debug("🧪 h_tarScan.finished 연결 완료")

            self.thread_tarScan.finished.connect(lambda: self.clean_up_scan(self.h_tarScan, self.thread_tarScan))
            self.scanlogger.debug("🧪 thread_tarScan.finished 연결 완료")

            self.thread_tarScan.start()

        self.ui._scan_tar_btn_back_to_ScanMain.setEnabled(False)
        self.scanlogger.info("[SCAN START] - Targeted system scan started.")



    def start_ent_scan(self):
        # 현재 날짜와 시간을 이용하여 로깅 및 결과 저장을 위한 scanLog 폴더 생성
        now = datetime.now()
        scanStartDate = now.strftime("%Y-%m-%d")
        scanStartTime = now.strftime("%H-%M-%S")

        self._ent_current_scan_datetime = f"{scanStartDate}_{scanStartTime}"
        seperated_log_name              = f"entScan_{self._ent_current_scan_datetime}"
        scan_log_file                   = f"entScan_{scanStartDate}_{scanStartTime}.log"

        self._ent_current_scan_log_dir  = os.path.join(log_dir, scanStartDate, "scanLogs", seperated_log_name)
        os.makedirs(os.path.join(self._ent_current_scan_log_dir), exist_ok=True)

        # Entire Scan 로그 파일 설정
        self.set_scan_log_file(self._ent_current_scan_log_dir, scan_log_file, scan_type="entScan")
        logging.info("* checking Fox2AV.Main Singletone system..." + "\n\t▶ infection_registry ID: %s\n",
                     id(infection_registry))


        # 전체 시스템 검사 프로세스 시작 지점
        drive_list = sig2.get_drives()
        drive_queue = queue.Queue()
        for drive in drive_list:
            drive_queue.put(drive)

        self.h_entScan = req_Scan(sig2.scan_entire, drive_queue, File_Hash_List, File_Name_List)
        self.thread_entScan = QThread()
        self.h_entScan.moveToThread(self.thread_entScan)

        self.h_entScan.progress.connect(self.ent_update_progress)
        self.h_entScan.update_label.connect(self.ent_update_label)
        self.h_entScan.update_status.connect(self.ent_update_status)
        self.thread_entScan.started.connect(self.h_entScan.run)

        self.h_entScan.finished.connect(self.on_entScan_finished)
        self.thread_entScan.finished.connect(lambda: self.clean_up_scan(self.h_entScan, self.thread_entScan))

        self.thread_entScan.start()
        self.ui._scan_ent_btn_back_to_ScanMain.setEnabled(False)  # 스캔 중 버튼 비활성화
        self.scanlogger.info("[SCAN START] - Entire system scan started.")


    def stop_tar_scan(self):
        if self.h_tarScan:
            self.h_tarScan.stop() # 스레드 중지 요청
            # scanning stop process
            userStopReply = QMessageBox.information(self, "Confirm Fox2AV Virus Scanning Abortions", "Are you sure want to abort scanning?", QMessageBox.Ok)
            if userStopReply == QMessageBox.Ok:
                self.ui.stackedWidget.setCurrentWidget(self.ui.scan)
                self.ui.Scan_stackedWidget.setCurrentWidget(self.ui.Scan_Main)

            self.ui._scan_tar_current_scanFile.setText("Targedted virus scan process stopped by user.")
            self.ui._scan_tar_btn_back_to_ScanMain.setEnabled(True)
            logging.warning("[SCAN STOP] - Targedted virus scan process stopped by user.")

    def stop_ent_scan(self):
        if self.h_entScan:
            self.h_entScan.stop()
            # scanning stop process
            userStopReply = QMessageBox.information(self, "Confirm Fox2AV Virus Scan Abortions",
                                                    "Are you sure want to abort scanning?", QMessageBox.Ok)
            if userStopReply == QMessageBox.Ok:
                self.ui.stackedWidget.setCurrentWidget(self.ui.scan)
                self.ui.Scan_stackedWidget.setCurrentWidget(self.ui.Scan_Main)

            self.ui._scan_ent_current_scanFile.setText("Full virus scan process stopped by user.")
            self.ui._scan_ent_btn_back_to_ScanMain.setEnabled(True)
            logging.warning("[SCAN STOP] - Entire virus scan process stopped by user.")

    """ get log data """
    #######################################################################
    def make_log_list(self, log_dir_path):
        logging.info("User checked log report list")

        if not os.path.exists(log_dir_path):
            logging.warning(f"Directory {log_dir_path} does not exist.")
            return

        log_data = []  # 로그 데이터를 저장할 리스트

        try:
            for date_folder in os.listdir(log_dir_path): # 날짜별 폴더 탐색
                date_folder_path = os.path.join(log_dir_path, date_folder)
                if os.path.isdir(date_folder_path): # 날짜 폴더인지 확인 (폴더만 탐색)
                    for file_name in os.listdir(date_folder_path): # 일반 로그 (global_*.log) 가져오기
                        file_path = os.path.join(date_folder_path, file_name)
                        if os.path.isfile(file_path) and file_name.startswith("global_") and file_name.endswith(".log"):
                            creation_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                                          time.localtime(os.path.getctime(file_path)))
                            log_data.append((creation_time, "Global", file_name, file_path))

                    scan_logs_folder = os.path.join(date_folder_path, "scanLogs") # 스캔 로그 (scanLogs 폴더 내 로그) 가져오기
                    if os.path.exists(scan_logs_folder) and os.path.isdir(scan_logs_folder):
                        for file_name in os.listdir(scan_logs_folder):
                            file_path = os.path.join(scan_logs_folder, file_name)
                            if os.path.isfile(file_path) and file_name.endswith(".log"):
                                creation_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                                              time.localtime(os.path.getctime(file_path)))

                                # 로그 유형 확인 (entireScan, tarScan)
                                if file_name.startswith("entireScan_"):
                                    log_type = "Entire Scan"
                                elif file_name.startswith("tarScan_"):
                                    log_type = "Targeted Scan"
                                else:
                                    log_type = "Unknown"
                                log_data.append((creation_time, log_type, file_name, file_path))
        except Exception as e:
            logging.error(f"Error accessing files in {log_dir_path}: {e}")

        # UI 테이블 업데이트
        self.ui.log_report_table_widget.setRowCount(len(log_data))
        for row, (creation_time, log_type, file_name, file_path) in enumerate(log_data):
            self.ui.log_report_table_widget.setItem(row, 0, QTableWidgetItem(creation_time))    # 생성 날짜
            self.ui.log_report_table_widget.setItem(row, 1, QTableWidgetItem(log_type))         # 로그 타입
            self.ui.log_report_table_widget.setItem(row, 2, QTableWidgetItem(file_name))        # 파일 이름
            self.ui.log_report_table_widget.setItem(row, 3, QTableWidgetItem(file_path))        # 파일 경로

        logging.info(f"Total {len(log_data)} log files listed.")


    """ secure quarantine sector """
    ########################################################################
    def secure_quarantine_sector(self, sector_dir):
        """ 탐지된 후 격리된 악성파일에 대한 정보 사용자에게 보여주는 기능"""
        # 지정된 경로에서 파일 목록 가져오기
        sector_malware_files = os.listdir(sector_dir)

        if not sector_malware_files:
            print("quarantine is empty.")
            return

        for file_name in sector_malware_files:
            file_path = os.path.join(sector_dir, file_name)

            if os.path.isfile(file_path):
                original_name, original_ext = os.path.splitext(file_name) # 파일명을 확장자를 포함하여 분리

                if original_ext == ".fxav":
                    continue

                # 새로운 파일 이름을 생성 (ex: a.exe -> a.exe.fxav)
                new_file_name = f"{file_name}.fxav"
                new_file_path = os.path.join(sector_dir, new_file_name)

                os.rename(file_path, new_file_path)
                print(f"File renamed: {file_name} -> {new_file_name}")

    """ get threat reports data """
    ########################################################################
    def make_threat_report(self, threatLog_dir: str) -> List[Tuple[str, Any]]:
        data_dicts = []
        results: List[Tuple[str, Any]] = []

        for dirpath, _, filenames in os.walk(threatLog_dir):
            if "detectRes.json" in filenames:
                full_path = os.path.join(dirpath, "detectRes.json")
                data: Any = None
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except JSONDecodeError as e:
                    logging.warning(f"⚠️ {full_path} Failed to parsing log files..({e}), try read-line...")
                    data = []
                    with open(full_path, 'r', encoding='utf-8') as f:
                        for lineno, line in enumerate(f, start=1):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                                data.append(obj)
                            except JSONDecodeError as line_e:
                                logging.warning(f"⚠️ {full_path} line {lineno} parsing failed: {line_e}")
                    if not data:
                        data = None  # 모두 실패했으면 None으로 처리

                except Exception as e:
                    print(f"⚠️ {full_path} Failed to open threat log file : {e}")
                    data = None
                if data is not None:
                    results.append((full_path, data))

        for _path, data_list in results:
            if isinstance(data_list, list):
                data_dicts.extend(data_list)
            else:
                data_dicts.append(data_list)

        self.ui.threat_report_table_widget.setRowCount(len(results))
        for row, entry in enumerate(data_dicts):
            detection_name  = entry.get("Detection time")
            risk_level      = entry.get("Risk Level")
            file_name       = entry.get("File name")
            threat_name     = entry.get("Threat name")
            threat_path     = entry.get("Threat path")
            action          = entry.get("Action")
            Hash            = entry.get("md5 hash")
            scan_engine     = entry.get("Scan engine")

            self.ui.threat_report_table_widget.setItem(row, 0, QTableWidgetItem(detection_name))
            self.ui.threat_report_table_widget.setItem(row, 1, QTableWidgetItem(risk_level))
            self.ui.threat_report_table_widget.setItem(row, 2, QTableWidgetItem(file_name))
            self.ui.threat_report_table_widget.setItem(row, 3, QTableWidgetItem(threat_name))
            self.ui.threat_report_table_widget.setItem(row, 4, QTableWidgetItem(threat_path))
            self.ui.threat_report_table_widget.setItem(row, 5, QTableWidgetItem(action))
            self.ui.threat_report_table_widget.setItem(row, 6, QTableWidgetItem(Hash))
            self.ui.threat_report_table_widget.setItem(row, 7, QTableWidgetItem(scan_engine))

        self.ui.threat_report_table_widget.resizeColumnsToContents()



    """ get quarantine data """
    ########################################################################
    def make_quarantine_list(self, sector_dir):
        if not os.path.exists(sector_dir):
            logging.warning(f"Directory {sector_dir} does not exist.")
            return

        # check qurantined data path and check exists
        dat_path = get_set_data("Quarantine", "qurantined_data_file_path")
        if not os.path.exists(dat_path):
            logging.warning(f"Directory {dat_path} does not exist.")
            return
        elif os.path.exists(dat_path):
            sector_secured_files = os.listdir(sector_dir)
            self.ui.quarantine_table_widget.setRowCount(len(sector_secured_files))  # 실행 파일 개수만큼 행 설정

            with open(dat_path, "r", encoding="utf-8") as f:
                entries = [
                    json.loads(line)
                    for line in f
                    if line.strip()
                ]
            for row, file_name in enumerate(sector_secured_files):
                file_path = os.path.join(sector_dir, file_name)
                if os.path.isfile(file_path):
                    for entry in entries:
                        fname = entry.get("File name")
                        if os.path.splitext(fname)[0] == os.path.splitext(file_name)[0]:
                            detection_time  = entry.get("Detection time")
                            threat_name     = entry.get("Threat name")
                            file_name       = entry.get("File name")
                            action          = entry.get("Action")
                            threat_path     = entry.get("Threat path")

                            self.ui.quarantine_table_widget.setItem(row, 0, QTableWidgetItem(detection_time))  # 격리된 날짜
                            self.ui.quarantine_table_widget.setItem(row, 1, QTableWidgetItem(threat_name))  # 탐지명
                            self.ui.quarantine_table_widget.setItem(row, 2, QTableWidgetItem(file_name))  # 파일 이름
                            self.ui.quarantine_table_widget.setItem(row, 3, QTableWidgetItem(action))  # 처리 결과
                            self.ui.quarantine_table_widget.setItem(row, 4, QTableWidgetItem(threat_path))  # 탐지된 파일 경로

    """ on remove btn clicked at Quarantine page """
    ########################################################################
    def remove_quarantined_files(self, sector_dir):
        self.play_sound_effect("deleted")
        if not os.path.exists(sector_dir):
            logging.warning(f"Directory {sector_dir} does not exist.")


    def on_Quarantine_remove_clicked(self):
        logging.info("on Quarantine remove clicked")
        self.play_sound_effect("error2")
        ret = QMessageBox.question(
            self,
            "Please Confirm",
            "You are trying to delete all quarantined malware files at malware sector. do you want to delete it?",
            QMessageBox.Ok | QMessageBox.Cancel
        )
        if ret == QMessageBox.Ok:
            self.remove_quarantined_files(qurantine_sector_dir)
        else:
            self.play_sound_effect("clicked")
            logging.info("User cancelled delete malware files.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())