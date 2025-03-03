import logging
import os
from itertools import count

## ==> import Fox2Av core libs
from Fox2Av.Foxcore.Signature_ScanEngine import Matching_Hash_Value

## ==> Global variables
from Fox2Av.Foxcore.singletone import infection_registry

black_list_path = [
    'Windows/CSC',                                  # 오프라인 파일 캐시 디렉터리
    'Windows/Fonts',                                # 시스템 폰트 디렉터리
    'Windows/INF',                                  # Windows 드라이버 INF 파일
    'Windows/Debug',                                # 디버그 로그
    'Windows/Logs',                                 # Windows 로그 파일 디렉터리
    'Windows/Assembly',                             # 글로벌 어셈블리 캐시(GAC)
    'Windows/Prefetch',                             # Windows Prefetch 파일
    'Windows/Minidump',                             # 시스템 충돌 덤프 파일
    'Windows/servicing',                            # Windows Servicing 디렉터리
    'Windows/Globalization',                        # 언어 및 지역 설정 디렉터리
    'Windows/SystemResources',                      # 시스템 리소스
    'ProgramData/Microsoft/Windows/WER',            # Windows Error Reporting (WER) 디렉터리
    'ProgramData/Microsoft/Windows Defender',       # Windows Defender 데이터 디렉터리
    'AppData/Roaming/Microsoft/Windows/Recent',     # 최근 문서
    'AppData/LocalLow/Microsoft/CryptnetUrlCache'   # 암호화 URL 캐시
]
black_list_file = [
    'ntldr'                             # NT 로더
    'bootmgr',                          # 부팅 관리자
    'hiberfil.sys',                     # 하이버네이션 파일
    'Windows/System32/dwm.exe',         # 데스크톱 창 관리자
    'Windows/System32/lsass.exe',       # 로컬 보안 인증 서버
    'Windows/System32/svchost.exe',     # 서비스 호스트 프로세스
    'Windows/System32/winlogon.exe',    # 사용자 로그인 관리 파일
    'Windows/System32/services.exe',    # 시스템 서비스 매니저
    'Windows/System32/explorer.exe',    # Windows 탐색기
    'Windows/System32/taskhostw.exe'   # 작업 호스트
]
excluded_extensions = [
    '.etl',       # 이벤트 추적 로그
    '.evtx',      # Windows 이벤트 로그
    '.cab',       # Windows 업데이트 압축 파일
    '.msi',       # Windows 설치 관리자 파일
    '.bak',       # 백업 파일
    '.mdmp',      # 메모리 덤프 파일
    '.dmp',       # 시스템 덤프 파일
    '.tmp', '.sys', '.log', '.dat',  # 임시, 시스템, 로그, 데이터 파일
    '.pagefile', '.swapfile', '.hiberfil',  # 가상 메모리, 하이버네이션 파일

    '.ggpk' # Path of Exile 대용량 파일
]

# 스캔에서 제외할 압축 파일 확장자 목록
compressed_file_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz']

# 1GB 이상 크기의 파일을 제외하는 기준 (1GB = 1,073,741,824 바이트)
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024


def get_drives():
    drives = []
    for drive in range(ord('A'), ord('Z') + 1):
        drive_letter = f"{chr(drive)}:\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives


def scan_entire(drive_queue, progress_callback, update_label_callback, stop_event, file_hash_list, file_name_list):
    total_drives = drive_queue.qsize()
    processed_files = 0
    estimated_total_files = 50000 * total_drives  # 초기 예상 파일 수 (드라이브 수 반영)

    while not drive_queue.empty():
        if stop_event.is_set():
            break

        drive = drive_queue.get()
        update_label_callback(f"Processing drive: {drive}")
        logging.debug(f"Scanning drive: {drive}")

        for root, dirs, files in os.walk(drive):
            if any(black_path in root for black_path in black_list_path):  # 블랙리스트 경로 확인
                continue

            for file_name in files:
                if stop_event.is_set():  # 사용자가 작업을 중단할 시
                    break

                file_path = os.path.join(root, file_name)

                # 블랙리스트 파일 및 확장자 확인
                if any(black_file in file_path for black_file in black_list_file):
                    continue
                if any(file_path.endswith(ext) for ext in excluded_extensions):
                    continue

                # 압축 파일이 아니면서 1GB 이상인 파일을 스캔 생략 (os.scandir() 사용)
                if not any(file_name.lower().endswith(ext) for ext in compressed_file_extensions):
                    try:
                        with os.scandir(root) as entries:
                            for entry in entries:
                                if entry.is_file():
                                    if entry.name == file_name and entry.stat().st_size > MAX_FILE_SIZE:
                                        logging.debug(
                                            f"Skipping large file: {entry.path} (Size: {entry.stat().st_size} bytes)")
                                        continue
                    except OSError as e:
                        logging.warning(f"Error accessing directory: {root} - {e}")
                        continue

                update_label_callback(file_path)

                # 감염 여부 검사
                if Matching_Hash_Value(file_path, file_hash_list, file_name_list) == 1:
                    infection_registry.add_infection(file_path)
                    logging.debug(f"Infection added: {file_path}")

                # 파일 단위로 진행률 업데이트
                processed_files += 1

                # 예상 파일 수가 적으면 동적으로 증가 (진행률을 너무 빨리 100%로 가는 것 방지)
                if processed_files > estimated_total_files * 0.9:
                    estimated_total_files = int(estimated_total_files * 1.5)
                    logging.debug(f"Adjusting estimated total files to: {estimated_total_files}")

                # 실시간 진행률 계산 (최대 99%까지)
                progress = min(int((processed_files / estimated_total_files) * 100), 99)
                progress_callback(progress)
                logging.debug(f"File processed: {file_path}, Progress: {progress}%")

    # 작업 완료 시 ProgressBar를 100%로 설정
    progress_callback(100)
    update_label_callback("Scan completed.")
    logging.info("Entire scan completed successfully.")



def scan_targeted(drive_queue, progress_callback, update_label_callback, stop_event, file_hash_list, file_name_list):
    processed_files = 0
    estimated_total_files = 80000  # 초기 임의의 예상 파일 수 (실시간으로 조정 가능)

    while not drive_queue.empty():
        if stop_event.is_set():
            break

        drive = drive_queue.get()
        update_label_callback(f"Processing drive: {drive}")
        logging.debug(f"Scanning drive: {drive}")

        for root, dirs, files in os.walk(drive):
            if any(black_path in root for black_path in black_list_path):  # 블랙리스트 경로 확인
                continue

            for file_name in files:
                if stop_event.is_set():  # 사용자가 작업을 중단할 시
                    break

                file_path = os.path.join(root, file_name)

                # 블랙리스트 파일 및 확장자 확인
                if any(black_file in file_path for black_file in black_list_file):
                    continue
                if any(file_path.endswith(ext) for ext in excluded_extensions):
                    continue

                # 압축 파일이 아니면서 1GB 이상인 파일을 스캔 생략 (os.scandir() 사용)
                if not any(file_name.lower().endswith(ext) for ext in compressed_file_extensions):
                    try:
                        with os.scandir(root) as entries:
                            for entry in entries:
                                if entry.is_file():
                                    if entry.name == file_name and entry.stat().st_size > MAX_FILE_SIZE:
                                        logging.debug(
                                            f"Skipping large file: {entry.path} (Size: {entry.stat().st_size} bytes)")
                                        continue
                    except OSError as e:
                        logging.warning(f"Error accessing directory: {root} - {e}")
                        continue

                update_label_callback(file_path)

                # 감염 여부 검사
                if Matching_Hash_Value(file_path, file_hash_list, file_name_list) == 1:
                    infection_registry.add_infection(file_path)
                    logging.debug(f"Infection added: {file_path}")

                # 파일 단위로 진행률 업데이트
                processed_files += 1

                # 예상 파일 수가 적으면 동적으로 증가 (진행률을 너무 빨리 100%로 가는 것 방지)
                if processed_files > estimated_total_files * 0.9:
                    estimated_total_files = int(estimated_total_files * 1.5)
                    logging.debug(f"Adjusting estimated total files to: {estimated_total_files}")

                # 실시간 진행률 계산 (최대 99%까지)
                progress = min(int((processed_files / estimated_total_files) * 100), 99)
                progress_callback(progress)
                logging.debug(f"File processed: {file_path}, Progress: {progress}%")

    # 작업 완료 시 ProgressBar를 100%로 설정
    progress_callback(100)
    update_label_callback("Scan completed.")
    logging.info("Targeted scan completed successfully.")




def scan_single(target_file_path, progress_callback, update_label_callback, stop_event, file_hash_list, file_name_list):
    if not os.path.exists(target_file_path):
        update_label_callback(f"Path does not exist: {target_file_path}")
        return

    total_files = sum(len(files) for _, _, files in os.walk(target_file_path))
    processed_files = 0

    update_label_callback(f"Processing path: {target_file_path}")

    for root, dirs, files in os.walk(target_file_path):
        if any(black_item in root for black_item in black_list_path):
            continue

        for file_name in files:
            if stop_event.is_set():
                update_label_callback("Scan stopped by user.")
                return

            file_path = os.path.join(root, file_name)

            # 블랙리스트 확장자 확인
            if any(file_name.lower().endswith(ext) for ext in excluded_extensions):
                continue

            # 압축 파일이 아니면서 1GB 이상인 파일을 스캔 생략
            if not any(file_name.lower().endswith(ext) for ext in compressed_file_extensions):
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > MAX_FILE_SIZE:
                        print(f"Skipping large file: {file_path} (Size: {file_size} bytes)")
                        continue
                except OSError as e:
                    print(f"Error accessing file: {file_path} - {e}")
                    continue

            update_label_callback(file_path)

            compareRes, malHash, malName = Matching_Hash_Value(file_path, file_hash_list, file_name_list)
            if compareRes:
                infection_registry.add_infection(file_path, malHash, malName)

            processed_files += 1
            progress_callback(int((processed_files / total_files) * 100))

    update_label_callback("Scan completed.")

