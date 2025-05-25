# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainVDpPAA.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGroupBox,
    QHeaderView, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QStackedWidget, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QWidget)
import resources_rc

class Ui_Fox2Av(object):
    def setupUi(self, Fox2Av):
        if not Fox2Av.objectName():
            Fox2Av.setObjectName(u"Fox2Av")
        Fox2Av.resize(1100, 680)
        Fox2Av.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.MainFrame = QFrame(Fox2Av)
        self.MainFrame.setObjectName(u"MainFrame")
        self.MainFrame.setGeometry(QRect(190, -10, 911, 691))
        self.MainFrame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.MainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.MainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.stackedWidget = QStackedWidget(self.MainFrame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 50, 911, 641))
        self.monitoring = QWidget()
        self.monitoring.setObjectName(u"monitoring")
        self.monitoring.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.monitoring_mainFrame = QFrame(self.monitoring)
        self.monitoring_mainFrame.setObjectName(u"monitoring_mainFrame")
        self.monitoring_mainFrame.setGeometry(QRect(0, -50, 961, 691))
        self.monitoring_mainFrame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.monitoring_mainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.monitoring_mainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.mon_img_main = QLabel(self.monitoring_mainFrame)
        self.mon_img_main.setObjectName(u"mon_img_main")
        self.mon_img_main.setGeometry(QRect(50, 260, 811, 231))
        self.mon_img_main.setStyleSheet(u"background-color: rgb(0, 255, 127);\n"
"background-image: url(:/png/images/mainImg.png);\n"
"border-radius: 15px;")
        self.recentFrame = QFrame(self.monitoring_mainFrame)
        self.recentFrame.setObjectName(u"recentFrame")
        self.recentFrame.setGeometry(QRect(50, 520, 251, 131))
        self.recentFrame.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 3px solid rgb(218, 218, 218);\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.recentFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.recentFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.mon_db_ver_info_title = QLabel(self.recentFrame)
        self.mon_db_ver_info_title.setObjectName(u"mon_db_ver_info_title")
        self.mon_db_ver_info_title.setGeometry(QRect(10, 30, 221, 31))
        self.mon_db_ver_info_title.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;")
        self.mon_db_ver_info_data = QLabel(self.recentFrame)
        self.mon_db_ver_info_data.setObjectName(u"mon_db_ver_info_data")
        self.mon_db_ver_info_data.setGeometry(QRect(20, 70, 211, 31))
        self.mon_db_ver_info_data.setStyleSheet(u"font: 10pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: rgb(126, 255, 255);\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;\n"
"qproperty-alignment: 'AlignCenter';")
        self.sfInfoFrame = QFrame(self.monitoring_mainFrame)
        self.sfInfoFrame.setObjectName(u"sfInfoFrame")
        self.sfInfoFrame.setGeometry(QRect(330, 520, 251, 131))
        self.sfInfoFrame.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 3px solid rgb(218, 218, 218);\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.sfInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.sfInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.mon_rt_status_title = QLabel(self.sfInfoFrame)
        self.mon_rt_status_title.setObjectName(u"mon_rt_status_title")
        self.mon_rt_status_title.setGeometry(QRect(20, 70, 181, 31))
        self.mon_rt_status_title.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;")
        self.mon_rt_status_data = QLabel(self.sfInfoFrame)
        self.mon_rt_status_data.setObjectName(u"mon_rt_status_data")
        self.mon_rt_status_data.setGeometry(QRect(200, 70, 41, 31))
        self.mon_rt_status_data.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: rgb(126, 255, 255);\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;")
        self.mon_autoScan_status_title = QLabel(self.sfInfoFrame)
        self.mon_autoScan_status_title.setObjectName(u"mon_autoScan_status_title")
        self.mon_autoScan_status_title.setGeometry(QRect(20, 30, 181, 31))
        self.mon_autoScan_status_title.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;")
        self.mon_autoScan_status_data = QLabel(self.sfInfoFrame)
        self.mon_autoScan_status_data.setObjectName(u"mon_autoScan_status_data")
        self.mon_autoScan_status_data.setGeometry(QRect(200, 30, 41, 31))
        self.mon_autoScan_status_data.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: rgb(126, 255, 255);\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;")
        self.malDBInfoFrame = QFrame(self.monitoring_mainFrame)
        self.malDBInfoFrame.setObjectName(u"malDBInfoFrame")
        self.malDBInfoFrame.setGeometry(QRect(610, 520, 251, 131))
        self.malDBInfoFrame.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 3px solid rgb(218, 218, 218);\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.malDBInfoFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.malDBInfoFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.mon_recentScanDate_Title = QLabel(self.malDBInfoFrame)
        self.mon_recentScanDate_Title.setObjectName(u"mon_recentScanDate_Title")
        self.mon_recentScanDate_Title.setGeometry(QRect(30, 30, 201, 31))
        self.mon_recentScanDate_Title.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;")
        self.mon_recentScanDate_data = QLabel(self.malDBInfoFrame)
        self.mon_recentScanDate_data.setObjectName(u"mon_recentScanDate_data")
        self.mon_recentScanDate_data.setGeometry(QRect(40, 70, 171, 31))
        self.mon_recentScanDate_data.setStyleSheet(u"font: 11pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: rgb(126, 255, 255);\n"
"background-color: rgb(32, 41, 64);\n"
"border: none;\n"
"border-radius: none;\n"
"padding: 4px 5px;\n"
"qproperty-alignment: 'AlignCenter';")
        self.gb_softwareInfo = QGroupBox(self.monitoring_mainFrame)
        self.gb_softwareInfo.setObjectName(u"gb_softwareInfo")
        self.gb_softwareInfo.setGeometry(QRect(50, 100, 811, 131))
        self.gb_softwareInfo.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.txt_softwareInfo = QLabel(self.gb_softwareInfo)
        self.txt_softwareInfo.setObjectName(u"txt_softwareInfo")
        self.txt_softwareInfo.setEnabled(False)
        self.txt_softwareInfo.setGeometry(QRect(35, 44, 741, 51))
        self.txt_softwareInfo.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.stackedWidget.addWidget(self.monitoring)
        self.scan = QWidget()
        self.scan.setObjectName(u"scan")
        self.Scan_stackedWidget = QStackedWidget(self.scan)
        self.Scan_stackedWidget.setObjectName(u"Scan_stackedWidget")
        self.Scan_stackedWidget.setGeometry(QRect(0, 0, 901, 641))
        self.Scan_Main = QWidget()
        self.Scan_Main.setObjectName(u"Scan_Main")
        self.Scan_mainFrame = QFrame(self.Scan_Main)
        self.Scan_mainFrame.setObjectName(u"Scan_mainFrame")
        self.Scan_mainFrame.setGeometry(QRect(0, 20, 931, 711))
        self.Scan_mainFrame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.Scan_mainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.Scan_mainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.Frame_Targeted_Scan = QFrame(self.Scan_mainFrame)
        self.Frame_Targeted_Scan.setObjectName(u"Frame_Targeted_Scan")
        self.Frame_Targeted_Scan.setGeometry(QRect(70, 320, 221, 251))
        self.Frame_Targeted_Scan.setStyleSheet(u"background-color: rgb(32, 41, 64);\n"
"")
        self.Frame_Targeted_Scan.setFrameShape(QFrame.Shape.StyledPanel)
        self.Frame_Targeted_Scan.setFrameShadow(QFrame.Shadow.Raised)
        self.tar_img_Scan = QLabel(self.Frame_Targeted_Scan)
        self.tar_img_Scan.setObjectName(u"tar_img_Scan")
        self.tar_img_Scan.setEnabled(False)
        self.tar_img_Scan.setGeometry(QRect(80, 10, 61, 61))
        self.tar_img_Scan.setStyleSheet(u"image: url(:/png/images/scan/targeted_scan_negative.png);\n"
"background-color: rgb(32, 41, 64);")
        self.tar_btn_Scan = QPushButton(self.Frame_Targeted_Scan)
        self.tar_btn_Scan.setObjectName(u"tar_btn_Scan")
        self.tar_btn_Scan.setGeometry(QRect(50, 90, 121, 41))
        self.tar_btn_Scan.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.tar_sub_title = QLabel(self.Frame_Targeted_Scan)
        self.tar_sub_title.setObjectName(u"tar_sub_title")
        self.tar_sub_title.setGeometry(QRect(40, 150, 151, 41))
        self.tar_sub_title.setStyleSheet(u"font: bold 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.tar_sub_detail = QLabel(self.Frame_Targeted_Scan)
        self.tar_sub_detail.setObjectName(u"tar_sub_detail")
        self.tar_sub_detail.setGeometry(QRect(20, 190, 191, 51))
        self.tar_sub_detail.setStyleSheet(u"font: 10pt \"Consolas\";\n"
"font-weight: bold;\n"
"text-align: center;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.tar_img_Scan.raise_()
        self.tar_sub_title.raise_()
        self.tar_btn_Scan.raise_()
        self.tar_sub_detail.raise_()
        self.Frame_Entire_Scan = QFrame(self.Scan_mainFrame)
        self.Frame_Entire_Scan.setObjectName(u"Frame_Entire_Scan")
        self.Frame_Entire_Scan.setGeometry(QRect(350, 320, 221, 251))
        self.Frame_Entire_Scan.setStyleSheet(u"background-color: rgb(32, 41, 64);\n"
"")
        self.Frame_Entire_Scan.setFrameShape(QFrame.Shape.StyledPanel)
        self.Frame_Entire_Scan.setFrameShadow(QFrame.Shadow.Raised)
        self.ent_img_Scan = QLabel(self.Frame_Entire_Scan)
        self.ent_img_Scan.setObjectName(u"ent_img_Scan")
        self.ent_img_Scan.setEnabled(False)
        self.ent_img_Scan.setGeometry(QRect(80, 10, 61, 61))
        self.ent_img_Scan.setStyleSheet(u"image: url(:/png/images/scan/full_scan_negative.png);\n"
"background-color: rgb(32, 41, 64);")
        self.ent_btn_Scan = QPushButton(self.Frame_Entire_Scan)
        self.ent_btn_Scan.setObjectName(u"ent_btn_Scan")
        self.ent_btn_Scan.setGeometry(QRect(50, 90, 121, 41))
        self.ent_btn_Scan.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.ent_sub_detail = QLabel(self.Frame_Entire_Scan)
        self.ent_sub_detail.setObjectName(u"ent_sub_detail")
        self.ent_sub_detail.setGeometry(QRect(35, 190, 151, 51))
        self.ent_sub_detail.setStyleSheet(u"font: 10pt \"Consolas\";\n"
"font-weight: bold;\n"
"text-align: center;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.ent_sub_title = QLabel(self.Frame_Entire_Scan)
        self.ent_sub_title.setObjectName(u"ent_sub_title")
        self.ent_sub_title.setGeometry(QRect(30, 150, 171, 41))
        self.ent_sub_title.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.ent_img_Scan.raise_()
        self.ent_sub_detail.raise_()
        self.ent_sub_title.raise_()
        self.ent_btn_Scan.raise_()
        self.Frame_Custom_Scan = QFrame(self.Scan_mainFrame)
        self.Frame_Custom_Scan.setObjectName(u"Frame_Custom_Scan")
        self.Frame_Custom_Scan.setGeometry(QRect(610, 320, 221, 251))
        self.Frame_Custom_Scan.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.Frame_Custom_Scan.setFrameShape(QFrame.Shape.StyledPanel)
        self.Frame_Custom_Scan.setFrameShadow(QFrame.Shadow.Raised)
        self.cus_img_Scan = QLabel(self.Frame_Custom_Scan)
        self.cus_img_Scan.setObjectName(u"cus_img_Scan")
        self.cus_img_Scan.setEnabled(False)
        self.cus_img_Scan.setGeometry(QRect(80, 10, 61, 61))
        self.cus_img_Scan.setStyleSheet(u"image: url(:/png/images/scan/custom_scan_negative.png);\n"
"background-color: rgb(32, 41, 64);")
        self.cus_btn_Scan = QPushButton(self.Frame_Custom_Scan)
        self.cus_btn_Scan.setObjectName(u"cus_btn_Scan")
        self.cus_btn_Scan.setGeometry(QRect(50, 90, 121, 41))
        self.cus_btn_Scan.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.cus_sub_detail = QLabel(self.Frame_Custom_Scan)
        self.cus_sub_detail.setObjectName(u"cus_sub_detail")
        self.cus_sub_detail.setGeometry(QRect(30, 190, 161, 41))
        self.cus_sub_detail.setStyleSheet(u"font: 10pt \"Consolas\";\n"
"font-weight: bold;\n"
"text-align: center;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.cus_sub_title = QLabel(self.Frame_Custom_Scan)
        self.cus_sub_title.setObjectName(u"cus_sub_title")
        self.cus_sub_title.setGeometry(QRect(50, 150, 131, 41))
        self.cus_sub_title.setStyleSheet(u"font: bold 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.scan_img_main = QLabel(self.Scan_mainFrame)
        self.scan_img_main.setObjectName(u"scan_img_main")
        self.scan_img_main.setGeometry(QRect(30, 30, 841, 231))
        self.scan_img_main.setStyleSheet(u"background-color: rgb(0, 255, 127);\n"
"background-image: url(:/png/images/mainImg.png);\n"
"border-radius: 15px;")
        self.Scan_stackedWidget.addWidget(self.Scan_Main)
        self._scan_set_targeted_page = QWidget()
        self._scan_set_targeted_page.setObjectName(u"_scan_set_targeted_page")
        self._scan_set_targeted_frame = QFrame(self._scan_set_targeted_page)
        self._scan_set_targeted_frame.setObjectName(u"_scan_set_targeted_frame")
        self._scan_set_targeted_frame.setGeometry(QRect(0, 10, 911, 631))
        self._scan_set_targeted_frame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self._scan_set_targeted_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self._scan_set_targeted_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._scan_set_tar_btn_back_to_ScanMain = QPushButton(self._scan_set_targeted_frame)
        self._scan_set_tar_btn_back_to_ScanMain.setObjectName(u"_scan_set_tar_btn_back_to_ScanMain")
        self._scan_set_tar_btn_back_to_ScanMain.setGeometry(QRect(450, 530, 91, 51))
        self._scan_set_tar_btn_back_to_ScanMain.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self._scan_set_tar_driveTree = QTreeWidget(self._scan_set_targeted_frame)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self._scan_set_tar_driveTree.setHeaderItem(__qtreewidgetitem)
        self._scan_set_tar_driveTree.setObjectName(u"_scan_set_tar_driveTree")
        self._scan_set_tar_driveTree.setGeometry(QRect(70, 120, 591, 141))
        self._scan_set_tar_driveTree.setStyleSheet(u"font: 13.5pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_set_tar_title_drive = QLabel(self._scan_set_targeted_frame)
        self._scan_set_tar_title_drive.setObjectName(u"_scan_set_tar_title_drive")
        self._scan_set_tar_title_drive.setGeometry(QRect(50, 80, 611, 31))
        self._scan_set_tar_title_drive.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_set_tar_title_folder = QLabel(self._scan_set_targeted_frame)
        self._scan_set_tar_title_folder.setObjectName(u"_scan_set_tar_title_folder")
        self._scan_set_tar_title_folder.setGeometry(QRect(50, 300, 441, 31))
        self._scan_set_tar_title_folder.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_set_tar_btn_openFolder = QPushButton(self._scan_set_targeted_frame)
        self._scan_set_tar_btn_openFolder.setObjectName(u"_scan_set_tar_btn_openFolder")
        self._scan_set_tar_btn_openFolder.setGeometry(QRect(60, 380, 301, 51))
        self._scan_set_tar_btn_openFolder.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self._scan_set_tar_title_detail_folder = QLabel(self._scan_set_targeted_frame)
        self._scan_set_tar_title_detail_folder.setObjectName(u"_scan_set_tar_title_detail_folder")
        self._scan_set_tar_title_detail_folder.setGeometry(QRect(70, 330, 781, 31))
        self._scan_set_tar_title_detail_folder.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_set_tar_btn_scannow = QPushButton(self._scan_set_targeted_frame)
        self._scan_set_tar_btn_scannow.setObjectName(u"_scan_set_tar_btn_scannow")
        self._scan_set_tar_btn_scannow.setGeometry(QRect(300, 530, 131, 51))
        self._scan_set_tar_btn_scannow.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: black;\n"
"background-color: rgb(0, 232, 0);\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self._scan_set_tar_locate = QLabel(self._scan_set_targeted_frame)
        self._scan_set_tar_locate.setObjectName(u"_scan_set_tar_locate")
        self._scan_set_tar_locate.setGeometry(QRect(10, 10, 291, 31))
        self._scan_set_tar_locate.setStyleSheet(u"font: bold 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_set_tar_arrow_icon1 = QLabel(self._scan_set_targeted_frame)
        self._scan_set_tar_arrow_icon1.setObjectName(u"_scan_set_tar_arrow_icon1")
        self._scan_set_tar_arrow_icon1.setEnabled(False)
        self._scan_set_tar_arrow_icon1.setGeometry(QRect(30, 80, 21, 31))
        self._scan_set_tar_arrow_icon1.setStyleSheet(u"image: url(:/png/images/Universal/right_arrow_negative.png);\n"
"background-color: rgb(32, 41, 64);")
        self._scan_set_tar_arrow_icon2 = QLabel(self._scan_set_targeted_frame)
        self._scan_set_tar_arrow_icon2.setObjectName(u"_scan_set_tar_arrow_icon2")
        self._scan_set_tar_arrow_icon2.setEnabled(False)
        self._scan_set_tar_arrow_icon2.setGeometry(QRect(30, 300, 21, 31))
        self._scan_set_tar_arrow_icon2.setStyleSheet(u"image: url(:/png/images/Universal/right_arrow_negative.png);\n"
"background-color: rgb(32, 41, 64);")
        self.Scan_stackedWidget.addWidget(self._scan_set_targeted_page)
        self._scan_entire_page = QWidget()
        self._scan_entire_page.setObjectName(u"_scan_entire_page")
        self._scan_entire_frame = QFrame(self._scan_entire_page)
        self._scan_entire_frame.setObjectName(u"_scan_entire_frame")
        self._scan_entire_frame.setGeometry(QRect(0, 10, 911, 631))
        self._scan_entire_frame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self._scan_entire_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self._scan_entire_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._scan_ent_btn_stop_scan = QPushButton(self._scan_entire_frame)
        self._scan_ent_btn_stop_scan.setObjectName(u"_scan_ent_btn_stop_scan")
        self._scan_ent_btn_stop_scan.setGeometry(QRect(310, 530, 131, 51))
        self._scan_ent_btn_stop_scan.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(223, 0, 0);\n"
"border-radius: 10px;\n"
"padding: 5px 10px;")
        self._scan_ent_btn_back_to_ScanMain = QPushButton(self._scan_entire_frame)
        self._scan_ent_btn_back_to_ScanMain.setObjectName(u"_scan_ent_btn_back_to_ScanMain")
        self._scan_ent_btn_back_to_ScanMain.setGeometry(QRect(460, 530, 91, 51))
        self._scan_ent_btn_back_to_ScanMain.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self._scan_ent_locate = QLabel(self._scan_entire_frame)
        self._scan_ent_locate.setObjectName(u"_scan_ent_locate")
        self._scan_ent_locate.setGeometry(QRect(10, 10, 301, 31))
        self._scan_ent_locate.setStyleSheet(u"font: bold 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_ent_title = QLabel(self._scan_entire_frame)
        self._scan_ent_title.setObjectName(u"_scan_ent_title")
        self._scan_ent_title.setGeometry(QRect(330, 70, 251, 31))
        self._scan_ent_title.setStyleSheet(u"font: 20pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_ent_sub_title = QLabel(self._scan_entire_frame)
        self._scan_ent_sub_title.setObjectName(u"_scan_ent_sub_title")
        self._scan_ent_sub_title.setGeometry(QRect(300, 110, 311, 31))
        self._scan_ent_sub_title.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_ent_processbar = QProgressBar(self._scan_entire_frame)
        self._scan_ent_processbar.setObjectName(u"_scan_ent_processbar")
        self._scan_ent_processbar.setGeometry(QRect(80, 297, 741, 21))
        self._scan_ent_processbar.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(98, 114, 164);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: none;\n"
"	border-radius: 10px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk {\n"
"	border-radius: 10px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.523, x2:1, y2:0.528, stop:0 rgba(255, 152, 219, 255), stop:1 rgba(170, 85, 255, 255));\n"
"}")
        self._scan_ent_processbar.setValue(0)
        self._scan_ent_current_scanFile = QLabel(self._scan_entire_frame)
        self._scan_ent_current_scanFile.setObjectName(u"_scan_ent_current_scanFile")
        self._scan_ent_current_scanFile.setGeometry(QRect(90, 328, 721, 31))
        self._scan_ent_current_scanFile.setStyleSheet(u"font: 12pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_ent_ScanStatus = QLabel(self._scan_entire_frame)
        self._scan_ent_ScanStatus.setObjectName(u"_scan_ent_ScanStatus")
        self._scan_ent_ScanStatus.setGeometry(QRect(350, 250, 201, 31))
        self._scan_ent_ScanStatus.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;\n"
"qproperty-alignment: 'AlignCenter';")
        self.Scan_stackedWidget.addWidget(self._scan_entire_page)
        self._scan_targeted_page = QWidget()
        self._scan_targeted_page.setObjectName(u"_scan_targeted_page")
        self._scan_targeted_frame = QFrame(self._scan_targeted_page)
        self._scan_targeted_frame.setObjectName(u"_scan_targeted_frame")
        self._scan_targeted_frame.setGeometry(QRect(0, 10, 911, 631))
        self._scan_targeted_frame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self._scan_targeted_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self._scan_targeted_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._scan_tar_btn_stop_scan = QPushButton(self._scan_targeted_frame)
        self._scan_tar_btn_stop_scan.setObjectName(u"_scan_tar_btn_stop_scan")
        self._scan_tar_btn_stop_scan.setGeometry(QRect(310, 530, 131, 51))
        self._scan_tar_btn_stop_scan.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(223, 0, 0);\n"
"border-radius: 10px;\n"
"padding: 5px 10px;")
        self._scan_tar_btn_back_to_ScanMain = QPushButton(self._scan_targeted_frame)
        self._scan_tar_btn_back_to_ScanMain.setObjectName(u"_scan_tar_btn_back_to_ScanMain")
        self._scan_tar_btn_back_to_ScanMain.setGeometry(QRect(460, 530, 91, 51))
        self._scan_tar_btn_back_to_ScanMain.setStyleSheet(u"font: 14pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self._scan_tar_locate = QLabel(self._scan_targeted_frame)
        self._scan_tar_locate.setObjectName(u"_scan_tar_locate")
        self._scan_tar_locate.setGeometry(QRect(10, 10, 301, 31))
        self._scan_tar_locate.setStyleSheet(u"font: bold 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_tar_title = QLabel(self._scan_targeted_frame)
        self._scan_tar_title.setObjectName(u"_scan_tar_title")
        self._scan_tar_title.setGeometry(QRect(300, 70, 301, 41))
        self._scan_tar_title.setStyleSheet(u"font: 20pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_tar_sub_title = QLabel(self._scan_targeted_frame)
        self._scan_tar_sub_title.setObjectName(u"_scan_tar_sub_title")
        self._scan_tar_sub_title.setGeometry(QRect(290, 110, 321, 31))
        self._scan_tar_sub_title.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_tar_processbar = QProgressBar(self._scan_targeted_frame)
        self._scan_tar_processbar.setObjectName(u"_scan_tar_processbar")
        self._scan_tar_processbar.setGeometry(QRect(80, 297, 741, 21))
        self._scan_tar_processbar.setStyleSheet(u"QProgressBar {\n"
"	\n"
"	background-color: rgb(98, 114, 164);\n"
"	color: rgb(200, 200, 200);\n"
"	border-style: none;\n"
"	border-radius: 10px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk {\n"
"	border-radius: 10px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.523, x2:1, y2:0.528, stop:0 rgba(255, 152, 219, 255), stop:1 rgba(170, 85, 255, 255));\n"
"}")
        self._scan_tar_processbar.setValue(0)
        self._scan_tar_current_scanFile = QLabel(self._scan_targeted_frame)
        self._scan_tar_current_scanFile.setObjectName(u"_scan_tar_current_scanFile")
        self._scan_tar_current_scanFile.setGeometry(QRect(90, 328, 721, 31))
        self._scan_tar_current_scanFile.setStyleSheet(u"font: 12pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self._scan_tar_ScanStatus = QLabel(self._scan_targeted_frame)
        self._scan_tar_ScanStatus.setObjectName(u"_scan_tar_ScanStatus")
        self._scan_tar_ScanStatus.setGeometry(QRect(350, 250, 201, 31))
        self._scan_tar_ScanStatus.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;\n"
"qproperty-alignment: 'AlignCenter';")
        self.Scan_stackedWidget.addWidget(self._scan_targeted_page)
        self.stackedWidget.addWidget(self.scan)
        self.report = QWidget()
        self.report.setObjectName(u"report")
        self.report_MainFrame = QFrame(self.report)
        self.report_MainFrame.setObjectName(u"report_MainFrame")
        self.report_MainFrame.setGeometry(QRect(-10, -50, 961, 691))
        self.report_MainFrame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.report_MainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.report_MainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.report_locate = QLabel(self.report_MainFrame)
        self.report_locate.setObjectName(u"report_locate")
        self.report_locate.setGeometry(QRect(20, 80, 211, 31))
        self.report_locate.setStyleSheet(u"font: bold 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.log_report_table_widget = QTableWidget(self.report_MainFrame)
        self.log_report_table_widget.setObjectName(u"log_report_table_widget")
        self.log_report_table_widget.setGeometry(QRect(50, 160, 821, 201))
        self.log_report_table_widget.setStyleSheet(u"background-color: rgb(32, 41, 64);\n"
"font: 9.5pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.log_report_table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.log_report_table_widget.setDragEnabled(False)
        self.log_report_table_widget.setSortingEnabled(True)
        self.threat_report_table_widget = QTableWidget(self.report_MainFrame)
        self.threat_report_table_widget.setObjectName(u"threat_report_table_widget")
        self.threat_report_table_widget.setGeometry(QRect(50, 420, 821, 241))
        self.threat_report_table_widget.setStyleSheet(u"background-color: rgb(32, 41, 64);\n"
"font: 9.5pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.threat_report_table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.threat_report_table_widget.setDragEnabled(False)
        self.log_report_title = QLabel(self.report_MainFrame)
        self.log_report_title.setObjectName(u"log_report_title")
        self.log_report_title.setGeometry(QRect(20, 120, 141, 31))
        self.log_report_title.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.threat_report_title = QLabel(self.report_MainFrame)
        self.threat_report_title.setObjectName(u"threat_report_title")
        self.threat_report_title.setGeometry(QRect(20, 380, 171, 31))
        self.threat_report_title.setStyleSheet(u"font: 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.stackedWidget.addWidget(self.report)
        self.Quarantine = QWidget()
        self.Quarantine.setObjectName(u"Quarantine")
        self.quarantine_MainFrame = QFrame(self.Quarantine)
        self.quarantine_MainFrame.setObjectName(u"quarantine_MainFrame")
        self.quarantine_MainFrame.setGeometry(QRect(0, -50, 961, 691))
        self.quarantine_MainFrame.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.quarantine_MainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.quarantine_MainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.qurantine_locate = QLabel(self.quarantine_MainFrame)
        self.qurantine_locate.setObjectName(u"qurantine_locate")
        self.qurantine_locate.setGeometry(QRect(10, 80, 301, 31))
        self.qurantine_locate.setStyleSheet(u"font: bold 13pt \"Consolas\";\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"padding: 4px 5px;")
        self.quarantine_table_widget = QTableWidget(self.quarantine_MainFrame)
        self.quarantine_table_widget.setObjectName(u"quarantine_table_widget")
        self.quarantine_table_widget.setGeometry(QRect(40, 140, 821, 471))
        self.quarantine_table_widget.setStyleSheet(u"background-color: rgb(32, 41, 64);\n"
"font: 11pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.quarantine_table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.quarantine_table_widget.setShowGrid(False)
        self.qurantine_delete_btn = QPushButton(self.quarantine_MainFrame)
        self.qurantine_delete_btn.setObjectName(u"qurantine_delete_btn")
        self.qurantine_delete_btn.setGeometry(QRect(660, 630, 201, 41))
        self.qurantine_delete_btn.setStyleSheet(u"font: 13.1pt \"Consolas\";\n"
"font-weight: bold;\n"
"color: white;\n"
"background-color: rgb(32, 41, 64);\n"
"border: 2px solid white;\n"
"border-radius: 10px;\n"
"padding: 4px 10px;")
        self.stackedWidget.addWidget(self.Quarantine)
        self.SubFrame = QFrame(Fox2Av)
        self.SubFrame.setObjectName(u"SubFrame")
        self.SubFrame.setGeometry(QRect(-10, -10, 201, 691))
        self.SubFrame.setStyleSheet(u"background-color: rgb(25, 33, 53);")
        self.SubFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.SubFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.lb_Monitoring = QFrame(self.SubFrame)
        self.lb_Monitoring.setObjectName(u"lb_Monitoring")
        self.lb_Monitoring.setEnabled(True)
        self.lb_Monitoring.setGeometry(QRect(10, 60, 191, 131))
        self.lb_Monitoring.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.lb_Monitoring.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_Monitoring.setFrameShadow(QFrame.Shadow.Raised)
        self.img_Monitoring = QLabel(self.lb_Monitoring)
        self.img_Monitoring.setObjectName(u"img_Monitoring")
        self.img_Monitoring.setEnabled(True)
        self.img_Monitoring.setGeometry(QRect(60, 30, 71, 51))
        self.img_Monitoring.setStyleSheet(u"image: url(:/png/images/subframe/monitoring_negative.png);")
        self.txt_Monitoring = QLabel(self.lb_Monitoring)
        self.txt_Monitoring.setObjectName(u"txt_Monitoring")
        self.txt_Monitoring.setEnabled(False)
        self.txt_Monitoring.setGeometry(QRect(40, 90, 111, 21))
        self.txt_Monitoring.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.btn_Monitoring = QPushButton(self.lb_Monitoring)
        self.btn_Monitoring.setObjectName(u"btn_Monitoring")
        self.btn_Monitoring.setGeometry(QRect(0, 0, 191, 131))
        self.btn_Monitoring.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.lb_Scan = QFrame(self.SubFrame)
        self.lb_Scan.setObjectName(u"lb_Scan")
        self.lb_Scan.setEnabled(True)
        self.lb_Scan.setGeometry(QRect(10, 190, 191, 131))
        self.lb_Scan.setStyleSheet(u"background-color: rgb(25, 33, 53);")
        self.lb_Scan.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_Scan.setFrameShadow(QFrame.Shadow.Raised)
        self.img_Scan = QLabel(self.lb_Scan)
        self.img_Scan.setObjectName(u"img_Scan")
        self.img_Scan.setEnabled(True)
        self.img_Scan.setGeometry(QRect(70, 30, 51, 51))
        self.img_Scan.setStyleSheet(u"image: url(:/png/images/subframe/scan_negative.png);")
        self.txt_Scan = QLabel(self.lb_Scan)
        self.txt_Scan.setObjectName(u"txt_Scan")
        self.txt_Scan.setEnabled(False)
        self.txt_Scan.setGeometry(QRect(40, 90, 121, 21))
        self.txt_Scan.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.btn_Scan = QPushButton(self.lb_Scan)
        self.btn_Scan.setObjectName(u"btn_Scan")
        self.btn_Scan.setGeometry(QRect(0, 0, 191, 131))
        self.btn_Scan.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.lb_Report = QFrame(self.SubFrame)
        self.lb_Report.setObjectName(u"lb_Report")
        self.lb_Report.setEnabled(True)
        self.lb_Report.setGeometry(QRect(10, 320, 191, 131))
        self.lb_Report.setStyleSheet(u"background-color: rgb(25, 33, 53);")
        self.lb_Report.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_Report.setFrameShadow(QFrame.Shadow.Raised)
        self.img_Report = QLabel(self.lb_Report)
        self.img_Report.setObjectName(u"img_Report")
        self.img_Report.setEnabled(True)
        self.img_Report.setGeometry(QRect(60, 30, 61, 51))
        self.img_Report.setStyleSheet(u"image: url(:/png/images/subframe/report_negative.png);")
        self.txt_Report = QLabel(self.lb_Report)
        self.txt_Report.setObjectName(u"txt_Report")
        self.txt_Report.setEnabled(False)
        self.txt_Report.setGeometry(QRect(60, 90, 71, 21))
        self.txt_Report.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.btn_report = QPushButton(self.lb_Report)
        self.btn_report.setObjectName(u"btn_report")
        self.btn_report.setGeometry(QRect(0, 0, 191, 131))
        self.btn_report.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.lb_Quarantine = QFrame(self.SubFrame)
        self.lb_Quarantine.setObjectName(u"lb_Quarantine")
        self.lb_Quarantine.setEnabled(True)
        self.lb_Quarantine.setGeometry(QRect(10, 450, 191, 131))
        self.lb_Quarantine.setStyleSheet(u"background-color: rgb(25, 33, 53);")
        self.lb_Quarantine.setFrameShape(QFrame.Shape.StyledPanel)
        self.lb_Quarantine.setFrameShadow(QFrame.Shadow.Raised)
        self.img_Quarantine = QLabel(self.lb_Quarantine)
        self.img_Quarantine.setObjectName(u"img_Quarantine")
        self.img_Quarantine.setEnabled(True)
        self.img_Quarantine.setGeometry(QRect(70, 30, 51, 51))
        self.img_Quarantine.setStyleSheet(u"image: url(:/png/images/subframe/sector_negative.png);")
        self.txt_Quarantine = QLabel(self.lb_Quarantine)
        self.txt_Quarantine.setObjectName(u"txt_Quarantine")
        self.txt_Quarantine.setEnabled(False)
        self.txt_Quarantine.setGeometry(QRect(50, 90, 101, 21))
        self.txt_Quarantine.setStyleSheet(u"font: 15pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.btn_Quarantine = QPushButton(self.lb_Quarantine)
        self.btn_Quarantine.setObjectName(u"btn_Quarantine")
        self.btn_Quarantine.setGeometry(QRect(0, 0, 191, 131))
        self.btn_Quarantine.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.fox2av_sub_Athor = QLabel(self.SubFrame)
        self.fox2av_sub_Athor.setObjectName(u"fox2av_sub_Athor")
        self.fox2av_sub_Athor.setGeometry(QRect(20, 660, 171, 21))
        self.fox2av_sub_Athor.setStyleSheet(u"font: 8pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.fox2av_sub_sfName = QLabel(self.SubFrame)
        self.fox2av_sub_sfName.setObjectName(u"fox2av_sub_sfName")
        self.fox2av_sub_sfName.setGeometry(QRect(20, 640, 131, 16))
        self.fox2av_sub_sfName.setStyleSheet(u"font: 10pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.FoxVcMenu = QFrame(Fox2Av)
        self.FoxVcMenu.setObjectName(u"FoxVcMenu")
        self.FoxVcMenu.setGeometry(QRect(0, 0, 1101, 51))
        self.FoxVcMenu.setStyleSheet(u"background-color: rgb(32, 41, 64);")
        self.FoxVcMenu.setFrameShape(QFrame.Shape.StyledPanel)
        self.FoxVcMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.fox2av_Name = QLabel(self.FoxVcMenu)
        self.fox2av_Name.setObjectName(u"fox2av_Name")
        self.fox2av_Name.setGeometry(QRect(48, 15, 101, 21))
        self.fox2av_Name.setStyleSheet(u"font: 22pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.fox2av_sub_Name = QLabel(self.FoxVcMenu)
        self.fox2av_sub_Name.setObjectName(u"fox2av_sub_Name")
        self.fox2av_sub_Name.setGeometry(QRect(157, 23, 270, 16))
        self.fox2av_sub_Name.setStyleSheet(u"font: 12pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        self.img_fox2av_logo = QLabel(self.FoxVcMenu)
        self.img_fox2av_logo.setObjectName(u"img_fox2av_logo")
        self.img_fox2av_logo.setGeometry(QRect(8, 10, 41, 31))
        self.img_fox2av_logo.setStyleSheet(u"image: url(:/png/images/logo_small.png);")
        self.sub_img_settings = QLabel(self.FoxVcMenu)
        self.sub_img_settings.setObjectName(u"sub_img_settings")
        self.sub_img_settings.setGeometry(QRect(860, 10, 31, 31))
        self.sub_img_settings.setStyleSheet(u"image: url(:/png/images/Universal/setting4_negative.png);")
        self.sub_txt_settings = QLabel(self.FoxVcMenu)
        self.sub_txt_settings.setObjectName(u"sub_txt_settings")
        self.sub_txt_settings.setGeometry(QRect(890, 5, 81, 41))
        self.sub_txt_settings.setStyleSheet(u"font: 10.5pt \"Consolas\";\n"
"font-weight: bold;\n"
"text-align: center;\n"
"color: white;\n"
"padding: 4px 5px;")
        self.sub_btn_minimalized = QPushButton(self.FoxVcMenu)
        self.sub_btn_minimalized.setObjectName(u"sub_btn_minimalized")
        self.sub_btn_minimalized.setGeometry(QRect(1015, 3, 41, 41))
        self.sub_btn_minimalized.setStyleSheet(u"image: url(:/png/images/Universal/minimalize_negative.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.sub_btn_close = QPushButton(self.FoxVcMenu)
        self.sub_btn_close.setObjectName(u"sub_btn_close")
        self.sub_btn_close.setGeometry(QRect(1058, 3, 41, 41))
        self.sub_btn_close.setStyleSheet(u"image: url(:/png/images/Universal/close_negative.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.sub_btn_settings = QPushButton(self.FoxVcMenu)
        self.sub_btn_settings.setObjectName(u"sub_btn_settings")
        self.sub_btn_settings.setGeometry(QRect(850, 0, 121, 51))
        self.sub_btn_settings.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.fox2av_Name.raise_()
        self.img_fox2av_logo.raise_()
        self.fox2av_sub_Name.raise_()
        self.sub_img_settings.raise_()
        self.sub_txt_settings.raise_()
        self.sub_btn_close.raise_()
        self.sub_btn_minimalized.raise_()
        self.sub_btn_settings.raise_()

        self.retranslateUi(Fox2Av)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Fox2Av)
    # setupUi

    def retranslateUi(self, Fox2Av):
        Fox2Av.setWindowTitle(QCoreApplication.translate("Fox2Av", u"Monitoring", None))
        self.mon_img_main.setText("")
        self.mon_db_ver_info_title.setText(QCoreApplication.translate("Fox2Av", u"Malware Pattern DB Version", None))
        self.mon_db_ver_info_data.setText(QCoreApplication.translate("Fox2Av", u"None", None))
        self.mon_rt_status_title.setText(QCoreApplication.translate("Fox2Av", u"Real-Time Protection", None))
        self.mon_rt_status_data.setText(QCoreApplication.translate("Fox2Av", u"Off", None))
        self.mon_autoScan_status_title.setText(QCoreApplication.translate("Fox2Av", u"Virus Scan Scheduler", None))
        self.mon_autoScan_status_data.setText(QCoreApplication.translate("Fox2Av", u"Off", None))
        self.mon_recentScanDate_Title.setText(QCoreApplication.translate("Fox2Av", u"Recent Virus Scan Date", None))
        self.mon_recentScanDate_data.setText(QCoreApplication.translate("Fox2Av", u"None", None))
        self.gb_softwareInfo.setTitle(QCoreApplication.translate("Fox2Av", u"Fox2Av - Reales news", None))
        self.txt_softwareInfo.setText(QCoreApplication.translate("Fox2Av", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">&quot;Fox2AV is a free and open-source antivirus solution designed for Windows,<br/>offering robust protection against malware and other security threats.&quot;</span></p></body></html>", None))
        self.tar_img_Scan.setText("")
        self.tar_btn_Scan.setText(QCoreApplication.translate("Fox2Av", u"Scan Now", None))
        self.tar_sub_title.setText(QCoreApplication.translate("Fox2Av", u"Targeted Scan", None))
        self.tar_sub_detail.setText(QCoreApplication.translate("Fox2Av", u"Scan specific folders or \n"
"external drives", None))
        self.ent_img_Scan.setText("")
        self.ent_btn_Scan.setText(QCoreApplication.translate("Fox2Av", u"Scan Now", None))
        self.ent_sub_detail.setText(QCoreApplication.translate("Fox2Av", u"Scan your entire PC \n"
"from top to bottom", None))
        self.ent_sub_title.setText(QCoreApplication.translate("Fox2Av", u"Full Virus Scan", None))
        self.cus_img_Scan.setText("")
        self.cus_btn_Scan.setText(QCoreApplication.translate("Fox2Av", u"Scan Now", None))
        self.cus_sub_detail.setText(QCoreApplication.translate("Fox2Av", u"Create your own scans", None))
        self.cus_sub_title.setText(QCoreApplication.translate("Fox2Av", u"Custom Scan", None))
        self.scan_img_main.setText("")
        self._scan_set_tar_btn_back_to_ScanMain.setText(QCoreApplication.translate("Fox2Av", u"Back", None))
        self._scan_set_tar_title_drive.setText(QCoreApplication.translate("Fox2Av", u"Please select the drive that you want the virus scan.", None))
        self._scan_set_tar_title_folder.setText(QCoreApplication.translate("Fox2Av", u"Detailed Directory Selection Features", None))
        self._scan_set_tar_btn_openFolder.setText(QCoreApplication.translate("Fox2Av", u"Open other location/folder", None))
        self._scan_set_tar_title_detail_folder.setText(QCoreApplication.translate("Fox2Av", u"Want to scan only certain directories, or don't have any folders you're looking for?", None))
        self._scan_set_tar_btn_scannow.setText(QCoreApplication.translate("Fox2Av", u"Scan Now", None))
        self._scan_set_tar_locate.setText(QCoreApplication.translate("Fox2Av", u"Fox2AV > Scan > Targeted Scan", None))
        self._scan_set_tar_arrow_icon1.setText("")
        self._scan_set_tar_arrow_icon2.setText("")
        self._scan_ent_btn_stop_scan.setText(QCoreApplication.translate("Fox2Av", u"Stop Scan", None))
        self._scan_ent_btn_back_to_ScanMain.setText(QCoreApplication.translate("Fox2Av", u"Back", None))
        self._scan_ent_locate.setText(QCoreApplication.translate("Fox2Av", u"Fox2AV > Scan > Full Virus Scan", None))
        self._scan_ent_title.setText(QCoreApplication.translate("Fox2Av", u"Full Virus Scan", None))
        self._scan_ent_sub_title.setText(QCoreApplication.translate("Fox2Av", u"Scan your entire PC top to bottom", None))
        self._scan_ent_current_scanFile.setText(QCoreApplication.translate("Fox2Av", u"Scanning :  ", None))
        self._scan_ent_ScanStatus.setText(QCoreApplication.translate("Fox2Av", u"Status", None))
        self._scan_tar_btn_stop_scan.setText(QCoreApplication.translate("Fox2Av", u"Stop Scan", None))
        self._scan_tar_btn_back_to_ScanMain.setText(QCoreApplication.translate("Fox2Av", u"Back", None))
        self._scan_tar_locate.setText(QCoreApplication.translate("Fox2Av", u"Fox2AV > Scan > Full Virus Scan", None))
        self._scan_tar_title.setText(QCoreApplication.translate("Fox2Av", u"Targeted Virus Scan", None))
        self._scan_tar_sub_title.setText(QCoreApplication.translate("Fox2Av", u"Scan your specific drives / folder", None))
        self._scan_tar_current_scanFile.setText(QCoreApplication.translate("Fox2Av", u"Scanning :  ", None))
        self._scan_tar_ScanStatus.setText(QCoreApplication.translate("Fox2Av", u"Status", None))
        self.report_locate.setText(QCoreApplication.translate("Fox2Av", u"Fox2AV > Report", None))
        self.log_report_title.setText(QCoreApplication.translate("Fox2Av", u"* scan report", None))
        self.threat_report_title.setText(QCoreApplication.translate("Fox2Av", u"* Threat report", None))
        self.qurantine_locate.setText(QCoreApplication.translate("Fox2Av", u"Fox2AV > Qurantine", None))
        self.qurantine_delete_btn.setText(QCoreApplication.translate("Fox2Av", u"Delete all malware", None))
        self.img_Monitoring.setText("")
        self.txt_Monitoring.setText(QCoreApplication.translate("Fox2Av", u"Monitoring", None))
        self.btn_Monitoring.setText("")
        self.img_Scan.setText("")
        self.txt_Scan.setText(QCoreApplication.translate("Fox2Av", u"Protection", None))
        self.btn_Scan.setText("")
        self.img_Report.setText("")
        self.txt_Report.setText(QCoreApplication.translate("Fox2Av", u"Report", None))
        self.btn_report.setText("")
        self.img_Quarantine.setText("")
        self.txt_Quarantine.setText(QCoreApplication.translate("Fox2Av", u"Qurantine", None))
        self.btn_Quarantine.setText("")
        self.fox2av_sub_Athor.setText(QCoreApplication.translate("Fox2Av", u"<html><head/><body><p>Athor by github.com/miho030</p></body></html>", None))
        self.fox2av_sub_sfName.setText(QCoreApplication.translate("Fox2Av", u"<html><head/><body><p>Fox2AV 1.2.8 -alpa</p></body></html>", None))
        self.fox2av_Name.setText(QCoreApplication.translate("Fox2Av", u"Fox2AV", None))
        self.fox2av_sub_Name.setText(QCoreApplication.translate("Fox2Av", u"OpenSource Anti-virus Solution", None))
        self.img_fox2av_logo.setText("")
        self.sub_img_settings.setText("")
        self.sub_txt_settings.setText(QCoreApplication.translate("Fox2Av", u"Settings", None))
        self.sub_btn_minimalized.setText("")
        self.sub_btn_close.setText("")
        self.sub_btn_settings.setText("")
    # retranslateUi

