import os.path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 악성코드 시그니처 예시 (간단한 문자열 패턴)
MALICIOUS_SIGNATURES = ["malware", "virus", "ransomware", "evil_code"]

# 파일 내용을 검사하는 함수
def scan_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for signature in MALICIOUS_SIGNATURES:
                if signature in content:
                    print(f"[!] 악성코드 시그니처 발견! 파일: {file_path}, 패턴: {signature}")
                    return True
        print(f"[OK] 안전한 파일: {file_path}")
    except Exception as e:
        print(f"[ERROR] 파일 검사 실패: {file_path}, 이유: {e}")
    return False

# 이벤트 핸들러 클래스
class RealTimeDetectionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"[INFO] 새 파일 생성됨: {event.src_path}")
            scan_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[INFO] 파일 수정됨: {event.src_path}")
            scan_file(event.src_path)

# 메인 함수
def main(directory_to_watch):
    print(f"[START] 실시간 탐지 엔진 시작: 감시 대상 디렉토리 -> {directory_to_watch}")
    event_handler = RealTimeDetectionHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("[STOP] 실시간 탐지 엔진 종료")
    observer.join()

# 감시할 디렉토리 설정
if __name__ == "__main__":
    directory = os.path.abspath("./")  # 감시할 디렉토리 경로
    main(directory)
