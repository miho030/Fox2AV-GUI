from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
import sys

class DetectionResultToast(QWidget):
    def __init__(self, total_infectedCount, infection_list, duration=5000, parent=None):
        super().__init__(parent)
        print("🧪 DetectionResultToast 생성됨")
        print("🧪 Toast __init__ 시작")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.resize(380, 210)

        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)


        # 제목 라벨
        if not infection_list:
            title = QLabel("✅ Virus scan completed! \t\t  Fox2AV-GUI")
        else:
            title = QLabel("⚠️ Malicious file found! \t    Fox2AV-GUI Alert")
        title.setStyleSheet("font-weight: bold; color: white; margin-bottom: 5px;")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title)

        # 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: rgb(32, 41, 64); border: none;")
        scroll_area.setAlignment(Qt.AlignHCenter)

        # 내용 위젯
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: rgb(32, 41, 64);")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)


        # 감염 항목 확인 후 추가
        if not infection_list:
            test_scan_type = "정밀 검사"
            scan_clean_res_text = (
                f"🛡️ Inspection Type: {test_scan_type}\n"
                f"🕒 Total scan time: -\n"
                f"📊 malware founded: 0 개\n"
                f"✅ No malware file found\n"
            )

            info_label = QLabel(scan_clean_res_text)
            info_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: rgb(32, 41, 64);
                    margin-bottom: 4px;
                }
            """)
            info_label.setWordWrap(True)
            info_label.setAlignment(Qt.AlignLeft)
            content_layout.addWidget(info_label)

        else:
            infectionCount = QLabel(f"Malware founded: {total_infectedCount} ea")
            infectionCount.setStyleSheet(
                "background-color: rgb(32, 41, 64); color: white; border: none; margin-bottom: 5px;")
            infectionCount.setWordWrap(True)
            infectionCount.setAlignment(Qt.AlignLeft)
            content_layout.addWidget(infectionCount)

            for file_path, file_name, file_hash, mal_name in infection_list:
                infection_info = (
                    f" 📁 name: {file_name}\n"
                    f" 🔗 path: {file_path}\n"
                    f" 🧬 hash: {file_hash}\n"
                    f" 💥 detection: {mal_name}\n"
                )

                res_label = QLabel(infection_info)
                res_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        background-color: rgb(32, 41, 64);
                        margin-bottom: 4px;
                    }
                """)
                res_label.setWordWrap(True)
                res_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                res_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                content_layout.addWidget(res_label)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # 우측 하단 위치에 창 띄우도록 설정
        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 40
            self.move(x, y)
        else:
            print("⚠️ Cannot get screen information..")
        """
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = screen_geometry.width() - self.width() - 20
        y = screen_geometry.height() - self.height() - 40
        self.move(x, y)
        """

        # 자동 닫기 → fade-out으로 변경
        QTimer.singleShot(duration, self.fade_out)

        self.setWindowOpacity(0.0) # Fade In 시작
        self.show()
        self.fade_in()

    def fade_in(self):
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_anim.setDuration(400)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(1.0)
        self.fade_in_anim.start()

    def fade_out(self):
        self.fade_out_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_anim.setDuration(400)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.finished.connect(self.close)
        self.fade_out_anim.start()


# 전역 참조 유지 리스트
_active_toasts = []
def show_detection_toast(total_infectedCount, detections, duration=5000, auto_quit=False, parent=None):
    if parent is None:
        parent = QApplication.activeWindow()

    toast = DetectionResultToast(total_infectedCount, detections, duration, parent=None)
    toast.setAttribute(Qt.WA_DeleteOnClose, True)
    _active_toasts.append(toast)

    QTimer.singleShot(100, toast.show)

    if auto_quit:
        QTimer.singleShot(duration + 4000, QApplication.instance().quit)


# 테스트 실행 코드
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sample_infectedCount = 2
    #sample_detections = []
    sample_detections = [
        [
            "E:/2_DEV/new_FoxVc/TestSector-MultiFile/AA.jpg",
            "AA.jpg",
            "79a8a749b5c377b21e574abd3d564579",
            "png.fox2av_RennkaTest.DUMMY.malware"
        ],
        [
            "E:/2_DEV/new_FoxVc/TestSector-MultiFile/TestSample.jpg",
            "TestSample.jpg",
            "79a8a749b5c377b21e574abd3d564579",
            "png.fox2av_RennkaTest.DUMMY.malware"
        ]
    ]
    show_detection_toast(sample_infectedCount, sample_detections)
    sys.exit(app.exec())
