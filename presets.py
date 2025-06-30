import os
import configparser

# 폴더 경로
logs_dir = os.path.abspath("./Common/Logs/")
settings_dir = os.path.abspath("./Common/Settings/")
quarantine_dir = os.path.abspath("./Common/Quarantine/")
sector_dir = os.path.abspath("./Common/Quarantine/Sectors/")

# 설정 파일 경로
settings_file_path = os.path.join(settings_dir, "fox2av_settings.ini")


def fox2av_preset_maker():
    # 폴더 생성
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(settings_dir, exist_ok=True)
    os.makedirs(quarantine_dir, exist_ok=True)
    os.makedirs(sector_dir, exist_ok=True)

def recent_scanDate_maker():
    print("fox2av-preset -- recent_scanDate_maker tester")

def fox2av_startup_set_manager():
    print("fox2av-preset -- fox2av_startup_set_manager tester")
    recent_scanDate_maker()

"""
프로그램 초기 설정 ini 파일임.
만약 사용자가 설정 초기화 버튼을 눌렀다면, ini 파일 삭제하고, 이 함수 실행하면 됨
"""
def reRoll_to_default_set():
    # 설정 파일 생성 및 작성
    config = configparser.ConfigParser()

    # 설정 파일의 기본 섹션 및 설정 값

    # 1. General Settings
    config['General'] = {
        'real_time_protection': 'off',
        'protection_mode': 'normal',
        'auto_update': 'disabled',
        'update_interval': '24',  # 시간 단위
        'setting_file_path': settings_file_path,
    }

    # 2. Network Settings
    config['Network'] = {
        'use_proxy': 'false',
        'proxy_address': '192.168.1.100',
        'proxy_port': '8080',
        'firewall_enabled': 'false',
        'allow_inbound_connections': 'true'
    }

    # 3. Scan Settings
    config['Scan'] = {
        'auto_virus_scan': 'off',
        'scan_time': '03:00',
        'scan_type': 'full',
        'exclusion_paths': 'C:\\Program Files\\Fox2av\\, C:\\Program Files\\Fox2av\\Common\\',
        'exclusion_files': 'fox2av.exe',
        'exclusion_extensions': '.fxav'
    }

    # 4. Notification Settings
    config['Notifications'] = {
        'show_notifications': 'true',
        'notification_sound': 'true',
        'critical_alerts_only': 'false',
        'log_path': 'C:\\Program Files\\Fox2av\\Logs\\',
        'log_level': 'verbose'
    }

    # 5. User Information
    config['User'] = {
        'license_key': 'ABCD-1234-EFGH-5678',
        'user_id': 'user1234',
        'registered': 'true'
    }

    # 6. Update Settings
    config['Update'] = {
        'last_update_dbVer': '0.0.3',
        'last_update_date': '2024-09-23',
        'latest_fox2av_version': '1.2.9',
        'update_server': 'update.antivirus.com',
        'fallback_server': 'backup.antivirus.com'
    }

    # 7. Quarantine Information
    config['Quarantine'] = {
        'auto_qurantine_option': 'true',
        'quarantine_master_path': quarantine_dir,
        'qurantine_path': sector_dir,
        'qurantined_data_file_path': quarantine_dir + "/" + "qurantined.dat",
        'quarantine_retention_days': '1000' # day
    }

    # 8. Scan History
    config['ScanHistory'] = {
        'last_scan_date': '2024-09-23 10:34:11',
        'last_scan_result': 'no threats found',
        'last_scan_duration': '00:15:23'
    }

    # 9. Exclusion Settings
    config['Exclusions'] = {
        'file_exclusions': 'C:\\Program Files\\SafeApp\\safeapp.exe',
        'folder_exclusions': 'D:\\Backup',
        'extension_exclusions': '.iso, .bak'
    }

    # 10. log settings
    config['Loggings'] = {
        'log_files_path': logs_dir
    }

    # 설정 파일이 없는 경우에만 생성
    if not os.path.exists(settings_file_path):
        with open(settings_file_path, 'w') as configfile:
            config.write(configfile)
