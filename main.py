################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##

"""
pyrcc5 -o resources_rc.py resources.qrc
"""
################################################################################

import os, sys, time
import threading, queue, configparser, logging
from datetime import datetime

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QAction, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *

## ==> for req scan
from PySide6.QtCore import  Signal, QObject, QThread, Slot
from PySide6.QtCore import Qt, QPoint, QRect, QPropertyAnimation, QEasingCurve, QEvent

## ==> GUI FILE
from ui_main import Ui_Fox2Av

## ==> import Fox2AV core
import Fox2Av.Foxcore.PlugInEngine.Signature as sig2
from Fox2Av.Foxcore.singletone import infection_registry

## ==> import Fox2AV programs
import presets as fox2av_presets

## ==> GLOBAL SETTINGS
DB_PATH = "./Fox2Av/Foxdb/main.hdb" # maleware DB
memory = 1024 * 100 # 102400
File_Hash_List, File_Size_List, File_Name_List = [], [],  []

log_dir = os.path.abspath("./Common/logs/")
quarantine_dir = os.path.abspath("./Common/Quarantine/")


""" Pre-load Fox2av presets """
fox2av_presets.fox2av_preset_maker()
fox2av_presets.reRoll_to_default_set()


def get_set_data(indexValue :str, keyValue :str):
    settings_file_path = os.path.join("./Common/Settings", "fox2av_settings.ini")
    config = configparser.ConfigParser()
    config.read(settings_file_path)
    read_setRes = config.get(indexValue, keyValue, fallback='N/A')

    return read_setRes


""" Pre-load malware database """
########################################################################
def DB_Pattern():
    with open(DB_PATH, "rb") as fdb:
        for hdb in fdb.readlines(memory):  # 지정된 메모리 안에서 DB를 불러옴
            hdb = hdb.decode('utf-8').strip()
            File_Hash_List.append(str(hdb.split(str(':'))[0]))  # DB에서 맨 앞부분(파일용량)부분만 잘라서 FSL(FileSizeList)에 추가
            File_Size_List.append(int(hdb.split(str(':'))[1]))  # DB에서 두번째 부분(파일md5해시)부분만 잘라서 FHL(FileHashList)
            File_Name_List.append(str(hdb.split(str(':'))[2]))  # DB에서 세번째 부분(파일 이름)부분 잘라서 FNL(FileNameList)
    return File_Hash_List, File_Size_List, File_Name_List

File_Hash_List, File_Size_List, File_Name_List = DB_Pattern() # Load the patterns into memory at startup


class req_Scan(QObject):
    progress = Signal(int)
    update_label = Signal(str)
    finished = Signal()

    def __init__(self, scan_function, drive_queue, file_hash_list, file_name_list):
        super().__init__()
        ##>> for scan process
        self._stop_event = threading.Event()
        self.scan_function = scan_function
        self.drive_queue = drive_queue
        self.file_hash_list = file_hash_list
        self.file_name_list = file_name_list

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
                self._stop_event,
                self.file_hash_list,
                self.file_name_list
            )
        except Exception as e:
            logging.debug(f"Exception in run method: {e}")
        finally:
            logging.debug(f"Senging Emitting finshed signal to scan engine..")
            self.finished.emit()  # ✅ 항상 finished 시그널을 호출하도록 보장


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Fox2Av()
        self.ui.setupUi(self)

        """ Fox2Av Startup Func """
        # 애플리케이션 시작 시 로그 설정 적용
        self.setup_logging()
        logging.info("Fox2AV-GUI Application started")

        # 모니터링 페이지 초기화 메서드 호출


        """ TOGGLE/BURGUER MENU """
        ########################################################################
        #self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        """ Windows settings """
        ########################################################################
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.oldPos = self.pos()


        """ GUI App SystemTry Settings """
        ########################################################################
        self.tray_icon = QSystemTrayIcon(self) # 시스템 트레이 아이콘 생성
        self.tray_icon.setIcon(QIcon("images/logo_small.png"))

        tray_menu = QMenu() # 트레이 아이콘 메뉴 생성

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

        ## ==>  Main Init
        self.ui.sub_btn_close.installEventFilter(self)
        self.ui.sub_btn_close.clicked.connect(self.close)
        self.ui.sub_btn_minimalized.clicked.connect(self.showMinimized)


        """ StackedWidget subFrame btn animation """
        ########################################################################
        ##>> for btn animations
        # 버튼 그룹 생성
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # 한 번에 하나의 버튼만 선택 가능
        self.buttons = [self.ui.btn_Monitoring, self.ui.btn_Scan, self.ui.btn_report, self.ui.btn_Quarantine]

        for idx, button in enumerate(self.buttons):
            button.setCheckable(True)  # 버튼을 체크할 수 있도록 설정
            self.button_group.addButton(button, idx)  # 버튼을 그룹에 추가
            button.clicked.connect(self.create_button_click_handler(idx))  # 클릭 핸들러 연결

        # 첫 번째 버튼을 기본 선택으로 설정
        self.buttons[0].setChecked(True)
        self.update_button_styles(0)


        """ Fox2Av PAGES Settings """
        ########################################################################
        ## ==> PAGE monitoring
        self.ui.btn_Monitoring.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.monitoring))
        # get data from ini file
        last_db_ver = get_set_data("Update", "last_update_dbVer")
        auto_scan_value = get_set_data("Scan", "auto_virus_scan")
        real_time_scan_value = get_set_data("General", "real_time_protection")
        recent_scan_date = get_set_data("ScanHistory", "last_scan_date")

        # set dashboard data from ini file
        self.ui.mon_db_ver_info_data.setText(last_db_ver)
        self.ui.mon_recentScanDate_data.setText(recent_scan_date)
        self.ui.mon_autoScan_status_data.setText(auto_scan_value)
        self.ui.mon_rt_status_data.setText(real_time_scan_value)

        ## ==> PAGE scan
        self.ui.btn_Scan.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.scan))

        ## ==> PAGE scan_Main
        self.ui.tar_btn_Scan.clicked.connect(lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_set_targeted_page))
        self.ui.ent_btn_Scan.clicked.connect(lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_entire_page))
        self.ui.ent_btn_Scan.clicked.connect(self.start_ent_scan)
        self.ui.cus_btn_Scan.clicked.connect(self.call_info_preparing)


        ## ==> PAGE _scan -> set_targeted_scan page
        self.ui._scan_set_tar_btn_openFolder.clicked.connect(self._scan_tar_open_dir)
        self.ui._scan_set_tar_btn_scannow.clicked.connect(lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_targeted_page))
        self.ui._scan_set_tar_btn_scannow.clicked.connect(self.start_tar_scan)
        self.ui._scan_set_tar_btn_back_to_ScanMain.clicked.connect(lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui.Scan_Main))


        # TreeWidget 헤더 숨기기
        self.ui._scan_set_tar_driveTree.setHeaderHidden(True)


        ## ==> PAGE _scan -> targeted_scan page
        self.ui._scan_tar_btn_back_to_ScanMain.clicked.connect(lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui._scan_set_targeted_page))
        self.ui._scan_tar_btn_stop_scan.clicked.connect(self.stop_tar_scan)

        ## ==> PAGE _scan -> entire_scan page
        self.ui._scan_ent_btn_back_to_ScanMain.clicked.connect(lambda: self.ui.Scan_stackedWidget.setCurrentWidget(self.ui.Scan_Main))
        self.ui._scan_ent_btn_stop_scan.clicked.connect(self.stop_ent_scan)


        ## ==> scan - custom_scan page

        ## ==> PAGE report
        self.ui.btn_report.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.report))

        self.ui.log_report_table_widget.setColumnCount(4)
        self.ui.log_report_table_widget.setHorizontalHeaderLabels(["Log creation date", "Log type", "File Name", "Log file path"])
        self.ui.log_report_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ui.threat_report_table_widget.setColumnCount(7)
        self.ui.threat_report_table_widget.setHorizontalHeaderLabels(["파일 이름", "위협 종류", "탐지명", "위협도", "처리 결과", "검사 유형", "탐지 날짜"])


        ## ==> PAGE sector
        self.ui.btn_Quarantine.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Quarantine))
        self.ui.quarantine_table_widget.setColumnCount(3)  # 3개의 열 설정
        self.ui.quarantine_table_widget.setHorizontalHeaderLabels(["File Name", "Creation Date", "Last Modified Date"])


        # ==> PAGE Repot,Qurantine 유저 친화 설정
        table_widgets = [
            self.ui.log_report_table_widget,
            self.ui.threat_report_table_widget,
            self.ui.quarantine_table_widget
        ]
        for table_widget in table_widgets:
            header = table_widget.horizontalHeader()
            for i in range(table_widget.columnCount()): # 모든 컬럼에 대해 자동 크기 조정 설정
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QHeaderView.Stretch) # 행 크기 자동 조절 (위젯에 맞게)

            header.setSectionsMovable(True) # 사용자가 컬럼을 이동 및 크기 조정할 수 있도록 설정
            header.setSectionsClickable(True)


        """ log 관련 기능 구현 """
        self.make_log_list(log_dir)
        log_report_layout = QVBoxLayout()
        log_report_layout.addWidget(self.ui.log_report_table_widget)
        self.setLayout(log_report_layout)

        threat_report_layout = QVBoxLayout()
        threat_report_layout.addWidget(self.ui.threat_report_table_widget)
        self.setLayout(threat_report_layout)


        """ Quarantine 관련 기능 구현 """
        self.make_quarantine_list(quarantine_dir)
        quarantine_layout = QVBoxLayout()
        quarantine_layout.addWidget(self.ui.quarantine_table_widget)
        self.setLayout(quarantine_layout)


        # 수평 헤더 (행,열 제목, 코너버튼) 배경색 변경
        self.ui.log_report_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.log_report_table_widget.verticalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.threat_report_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.threat_report_table_widget.verticalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(32, 41, 64);}")

        self.ui.quarantine_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(32, 41, 64);}")
        self.ui.quarantine_table_widget.verticalHeader().setStyleSheet("QHeaderView::section {background-color: rgb(32, 41, 64);}")


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


    """ Fox2AV Startup Func """
    def setup_logging(self):
        """ global 로그 파일 기록 관련 """
        # 현재 날짜, 시간 기반으로 파일 및 폴더 생성
        current_date = datetime.now().strftime("%Y-%m-%d")  # 폴더 이름 (YYYY-MM-DD 형식)
        current_time = datetime.now().strftime("%Y-%m-%d")  # 로그 파일 이름
        date_folder_path = os.path.join(log_dir, current_date)
        os.makedirs(date_folder_path, exist_ok=True)
        os.makedirs(os.path.join(date_folder_path, "scanLogs"), exist_ok=True)

        # 🌐 [1] 글로벌 로거 설정
        global_log_file_name = f"global_{current_time}.log"  # global 로그 파일 이름
        global_log_file_path = os.path.join(date_folder_path, global_log_file_name)
        logger = logging.getLogger() # global logger
        logger.setLevel(logging.INFO)

        # 로그 메시지 형식 설정
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        global_file_handler = logging.FileHandler(global_log_file_path) # 글로벌 로깅 핸들러
        global_file_handler.setFormatter(formatter)
        logger.addHandler(global_file_handler)

        global_console_handler = logging.StreamHandler() # 콘솔 핸들러 설정 (디버그 - 터미널에 출력)
        global_console_handler.setFormatter(formatter)
        logger.addHandler(global_console_handler)

        logging.info(f"Global Log file created: {global_log_file_path}")

        self.scanlogger = logging.getLogger("scanlogger") # 🛠️ [2] 스캔 전용 로거 (scanlogger) 초기화
        self.scanlogger.setLevel(logging.INFO)

        if len(self.scanlogger.handlers) > 0: # 기존 핸들러 제거 (중복 로그 방지)
            self.scanlogger.handlers.clear()


    def set_scan_log_file(self, scan_type="entireScan"):
        """ scan_type: "entireScan" 또는 "tarScan"을 지정하여 해당 로그 파일을 설정 """
        # 📅 현재 날짜와 시간을 이용하여 로그 파일명 생성
        current_date = datetime.now().strftime("%Y-%m-%d")  # 날짜별 폴더
        current_time = datetime.now().strftime("%H-%M-%S")  # 시간별 파일명
        log_file_name = f"{scan_type}_{current_date}_{current_time}.log"

        date_folder_path = os.path.join(log_dir, current_date) # 🗂️ 로그 파일 전체 경로 설정
        scan_log_dir = os.path.join(date_folder_path, "scanLogs/")
        scan_log_file = os.path.join(scan_log_dir, log_file_name)

        if len(self.scanlogger.handlers) > 0: # 기존 scanlogger 핸들러 초기화
            self.scanlogger.handlers.clear()

        # 로그 메시지 형식 설정
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(scan_log_file) # 새로운 파일 핸들러 설정
        file_handler.setFormatter(formatter)
        self.scanlogger.addHandler(file_handler)

        console_handler = logging.StreamHandler() # 콘솔 핸들러 설정 (디버그 - 터미널에 출력)
        console_handler.setFormatter(formatter)
        self.scanlogger.addHandler(console_handler)

        # 🚫 글로벌 로거로 로그 전파 방지
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
            "Fox2AV was minimized to the system tray.",
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
        # 윈도우 시스템에서 드라이브 목록 가져오기
        drives = []
        for drive in range(ord('A'), ord('Z') + 1):
            drive_letter = f"{chr(drive)}:\\"
            if os.path.exists(drive_letter):
                drives.append(drive_letter)
        return drives

    # Scan > Targeted Scan > open other folder
    def _scan_tar_open_dir(self):
        self.targeted_dir_name = QFileDialog.getExistingDirectory(self, 'Select folder','')
        return self.targeted_dir_name

    # Scan > Custom Scan > Scano now button
    def call_info_preparing(self):
        QMessageBox.information(self, "Information", "We are preparing this function!\nSee you soon XD")

    def call_info_cancled(self):
        QMessageBox.information(self, "Information", "Scanning stopped.")


    """ Fox2AV ANIMATION FUNCTIONS """
    ########################################################################
    def create_button_click_handler(self, index): # 버튼 클릭 시 실행되는 핸들러 생성 함수
        def handler():
            self.ui.stackedWidget.setCurrentIndex(index)  # 스택 페이지 전환
            self.update_button_styles(index)  # 버튼 배경 업데이트
        return handler

    def update_button_styles(self, clicked_index): # 버튼 스타일 업데이트 함수
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
            self.ui.sub_btn_close.setStyleSheet("image: url(:/png/images/Universal/hightited_close.png);background-color: rgb(32, 41, 64, 0);")
        elif event.type() == QEvent.Leave and source == self.ui.sub_btn_close:
            self.ui.sub_btn_close.setStyleSheet("image: url(:/png/images/Universal/close_negative.png);background-color: rgb(32, 41, 64, 0);")
        return super().eventFilter(source, event)



    """ Fox2AV MAIN FUNCTIONS """
    ########################################################################
    @Slot(int)
    def tar_update_progress(self, value):
        self.ui._scan_tar_processbar.setValue(value)

    @Slot(str)
    def tar_update_label(self, text):
        self.ui._scan_tar_current_scanFile.setText(text)

    @Slot(int)
    def ent_update_progress(self, value):
        self.ui._scan_ent_processbar.setValue(value)

    @Slot(str)
    def ent_update_label(self, text):
        self.ui._scan_ent_current_scanFile.setText(text)

    def clean_up_scan(self, scan_handler, scan_thread):
        """
        스레드와 핸들러를 안전하게 종료하고 메모리에서 삭제하는 함수.
        """
        try:
            # 1. 스레드가 실행 중인 경우 안전하게 종료
            if scan_thread and scan_thread.isRunning():
                logging.info("Thread is running, attempting to quit...")
                scan_thread.quit()
                scan_thread.wait()

            # 2. 안전하게 시그널 연결 해제 및 메모리 삭제
            if scan_handler:
                if scan_handler.signalsBlocked():
                    scan_handler.blockSignals(False)

                # 시그널 연결 해제 (이미 해제된 경우를 대비해 예외 처리)
                try:
                    if scan_handler.receivers(b"finished") > 0:
                        scan_handler.finished.disconnect()
                    if scan_handler.receivers(b"progress") > 0:
                        scan_handler.progress.disconnect()
                    if scan_handler.receivers(b"update_label") > 0:
                        scan_handler.update_label.disconnect()
                except (TypeError, RuntimeError) as e:
                    logging.warning(f"Handler signal already disconnected: {e}")

                # 안전하게 삭제 및 참조 해제
                scan_handler.deleteLater()
                self.h_tarScan = None
                self.h_entScan = None

            if scan_thread:
                try:
                    if scan_thread.receivers(b"finished") > 0:
                        scan_thread.finished.disconnect()
                except (TypeError, RuntimeError) as e:
                    logging.warning(f"Thread finished signal already disconnected: {e}")

                # 안전하게 삭제 및 참조 해제
                scan_thread.deleteLater()
                self.thread_tarScan = None
                self.thread_entScan = None

            logging.info("Scan and thread cleanup completed safely.")

        except Exception as e:
            logging.error(f"Error during scan cleanup: {e}")

    def start_tar_scan(self):
        checked_drive_list = []  # QTreeWidget에서 체크된 항목을 확인
        root = self.ui._scan_set_tar_driveTree.invisibleRootItem()
        child_count = root.childCount()

        for i in range(child_count):
            item = root.child(i)
            if item.checkState(0) == Qt.Checked:
                checked_drive_list.append(item.text(0))

        # QTreeWidget에서 체크된 항목도 없고, 사용자가 폴더도 선택하지 않은 경우 경고 메시지 출력
        if (checked_drive_list == None) and (self.targeted_dir_name == None):
            QMessageBox.warning(self, "경고", "스캔할 경로를 설정해주세요.")
            return

        if not (checked_drive_list == None) or (self.targeted_dir_name == None):
            drive_queue = queue.Queue()
            if checked_drive_list:
                for drive in checked_drive_list:
                    drive_queue.put(drive)
            else:
                drive_queue.put(self.targeted_dir_name)


            # 🗂️ Targeted Scan 로그 파일 설정
            self.set_scan_log_file(scan_type="tarScan")

            self.h_tarScan = req_Scan(sig2.scan_targeted, drive_queue, File_Hash_List, File_Name_List)
            self.thread_tarScan = QThread()
            self.h_tarScan.moveToThread(self.thread_tarScan)

            self.h_tarScan.progress.connect(self.tar_update_progress)
            self.h_tarScan.update_label.connect(self.tar_update_label)
            self.thread_tarScan.started.connect(self.h_tarScan.run)
            self.h_tarScan.finished.connect(
                lambda: [
                    logging.debug(f"Targeted scan engine received finished signal!"),
                    self.clean_up_scan(self.h_tarScan, self.thread_tarScan),
                    self.ui._scan_tar_btn_back_to_ScanMain.setEnabled(True),
                    self.scanlogger.info("[SCAN START] - Targeted system scan ended.")
                ]
            )

            self.thread_tarScan.start()

            """ 디버그 코드 시작 
            infections = infection_registry.get_infections()
            if not infections:
                QMessageBox.information(None, "감염된 파일 없음", "악성코드가 발견되지 않았습니다.")
                return
    
            # 감염된 파일들의 정보를 문자열로 생성
            infection_info = ""
            for file_path, file_name, file_hash in infections:
                infection_info += f"File Path: {file_path}\nFile Name: {file_name}\nFile Hash: {file_hash}\n\n"
    
            # 경고창으로 감염된 파일의 정보를 출력
            QMessageBox.warning(None, "악성코드 감지", infection_info)
            디버그 코드 종료 """

        self.ui._scan_tar_btn_back_to_ScanMain.setEnabled(False)
        self.scanlogger.info("[SCAN START] - Targeted system scan started.")


    def start_ent_scan(self):
        drive_list = sig2.get_drives()
        drive_queue = queue.Queue()
        for drive in drive_list:
            drive_queue.put(drive)

        # 🗂️ Entire Scan 로그 파일 설정
        self.set_scan_log_file(scan_type="entireScan")

        self.h_entScan = req_Scan(sig2.scan_entire, drive_queue, File_Hash_List, File_Name_List)
        self.thread_entScan = QThread()
        self.h_entScan.moveToThread(self.thread_entScan)

        # 시그널 연결
        self.h_entScan.progress.connect(self.ent_update_progress)
        self.h_entScan.update_label.connect(self.ent_update_label)
        self.thread_entScan.started.connect(self.h_entScan.run)
        self.thread_entScan.finished.connect(
            lambda: [
                self.clean_up_scan(self.h_entScan, self.thread_entScan),
                self.ui._scan_ent_btn_back_to_ScanMain.setEnabled(True),
                self.scanlogger.info("[SCAN START] - Entire system scan ended.")
            ]
        )

        self.thread_entScan.start()
        self.ui._scan_ent_btn_back_to_ScanMain.setEnabled(False) # 스캔 중 버튼 비활성화
        self.scanlogger.info("[SCAN START] - Entire system scan started.")



    def stop_tar_scan(self):
        if self.h_tarScan:
            self.h_tarScan.stop()
            # scanning stop process
            QMessageBox.information(self, "Information", "Scanning stopped.")
            self.ui._scan_tar_current_scanFile.setText("Targedted virus scan process stopped by user.")
            self.ui._scan_tar_btn_back_to_ScanMain.setEnabled(True)
            logging.warning("[SCAN STOP] - Targedted virus scan process stopped by user.")

    def stop_ent_scan(self):
        if self.h_entScan:
            self.h_entScan.stop()
            # scanning stop process
            QMessageBox.information(self, "Information", "Scanning stopped.")
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
            # 📁 날짜별 폴더 탐색 (예: 2025-03-02)
            for date_folder in os.listdir(log_dir_path):
                date_folder_path = os.path.join(log_dir_path, date_folder)

                # 날짜 폴더인지 확인 (폴더만 탐색)
                if os.path.isdir(date_folder_path):

                    # 🌐 [1] 일반 로그 (global_*.log) 가져오기
                    for file_name in os.listdir(date_folder_path):
                        file_path = os.path.join(date_folder_path, file_name)
                        if os.path.isfile(file_path) and file_name.startswith("global_") and file_name.endswith(".log"):
                            creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(file_path)))
                            log_data.append((creation_time, "Global", file_name, file_path))

                    # 🛠️ [2] 스캔 로그 (scanLogs 폴더 내 로그) 가져오기
                    scan_logs_folder = os.path.join(date_folder_path, "scanLogs")
                    if os.path.exists(scan_logs_folder) and os.path.isdir(scan_logs_folder):
                        for file_name in os.listdir(scan_logs_folder):
                            file_path = os.path.join(scan_logs_folder, file_name)
                            if os.path.isfile(file_path) and file_name.endswith(".log"):
                                creation_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(file_path)))

                                # 로그 유형 결정 (entireScan, tarScan)
                                if file_name.startswith("entireScan_"):
                                    log_type = "Entire Scan"
                                elif file_name.startswith("tarScan_"):
                                    log_type = "Targeted Scan"
                                else:
                                    log_type = "Unknown"
                                log_data.append((creation_time, log_type, file_name, file_path))
        except Exception as e:
            logging.error(f"Error accessing files in {log_dir_path}: {e}")

        # 📊 UI 테이블 업데이트
        self.ui.log_report_table_widget.setRowCount(len(log_data))
        for row, (creation_time, log_type, file_name, file_path) in enumerate(log_data):
            self.ui.log_report_table_widget.setItem(row, 0, QTableWidgetItem(creation_time))    # 생성 날짜
            self.ui.log_report_table_widget.setItem(row, 1, QTableWidgetItem(log_type))         # 로그 유형
            self.ui.log_report_table_widget.setItem(row, 2, QTableWidgetItem(file_name))        # 파일 이름
            self.ui.log_report_table_widget.setItem(row, 3, QTableWidgetItem(file_path))        # 파일 경로

        logging.info(f"Total {len(log_data)} log files listed.")

    """ get quarantine data """
    ########################################################################
    def make_quarantine_list(self, quarantine_dir):
        if not os.path.exists(quarantine_dir): # 지정된 경로에 격리된 파일이 있는지 확인
            logging.warning(f"Directory {quarantine_dir} does not exist.")
            return

        sector_malware_files = os.listdir(quarantine_dir) # 파일 목록 가져오기
        self.ui.quarantine_table_widget.setRowCount(len(sector_malware_files))  # 실행 파일 개수만큼 행 설정

        # 각 실행 파일에 대해 파일명, 생성 날짜, 수정 날짜 추가
        for row, file_name in enumerate(sector_malware_files):
            file_path = os.path.join(quarantine_dir, file_name)

            # 파일 정보 가져오기
            if os.path.isfile(file_path):  # 파일인 경우만 처리
                creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_path)))
                modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))

                # 파일 이름, 생성 날짜, 수정 날짜를 테이블에 추가
                self.ui.quarantine_table_widget.setItem(row, 0, QTableWidgetItem(file_name))  # 파일 이름
                self.ui.quarantine_table_widget.setItem(row, 1, QTableWidgetItem(creation_time))  # 생성 날짜
                self.ui.quarantine_table_widget.setItem(row, 2, QTableWidgetItem(modified_time))  # 수정 날짜


    """ secure quarantine sector """
    ########################################################################
    def secure_quarantine_sector(self, quarantine_dir):
        sector_malware_files = self.get_qurantine_file_list(quarantine_dir)
        """ 이 부분은 나중에, 악성코드들을 안전하게 격리하기 위한 확장자, fxav(또는 기타)만을 확인하여 가져오기 위한 내용을 담고있음
        executable_files = [f for f in files if f.endswith('.exe')]  # .exe 확장자 필터링

        # 실행 파일이 없을 경우
        if not executable_files:
            print("quarantine is empty.")
            return
        """
        """
        격리소 경로에 저장된 파일 중에 윈도우즈 시스템에서 실행 가능할만한 모든 확장자 파일들에 대해서 아래와 같이 파일의 확장자를 수정한다.
        ex) a.exe -> a.exe.fxav
        
        위의 같이 수정함으로서 파일의 임의 실행을 방지하고, 원래 어떤 확장자의 파일이었는지 split 가능하도록 수정
        
        
        격리소 관련 함수 2개 작성해야함.
        
            1. make_aurantine_list()
                - 격리소 대쉬보드 그려주는 부분
            2. secure_quarantine_sector()
                - 격리소 경로 내 위험 확장자를 전부 치환 하는 기능
                
        생각해야할 점은 secure_qurantine_sector()의 함수 호출 빈도 및 호출 부분을 설정해야할 필요가 있다.
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())