# -*- coding: utf-8 -*-

# Author : github.com/miho030

"""
해야할 것.
	1. 정상 작동 확인하기  --> 정상 작동 확인하였음.
	2. 불필요한 주석 제거하기  --> 불필요 주석 삭제 처리 완료
	3. 불필요한 라이브러리 import 없애기  --> 완료
	4. 라이브러리 종속성 해결 해야 하나?? 메인 파일에서 임포트 형식으로??   -> 그럴 필요는 없을듯
	5. 소스코드들 다듬기 (더욱 고수처럼 보이는 스킬 사용)
	5-1. 불필요한 소스코드 삭제하기  --> 불필요한 파일 삭제 조치 완료

	6. pretty print 등 이쁜 cli 출력을 위한 개조 기능 넣기
	7. log 생성 관련 함수, 호출, 내용 전부 삭제하기
	8. log 생성 관련 내용 다시 새롭게 작성하기 (직접 구현)
	9. 프로그램 속도 개선 (감염된 파일이 아니면 아무런 작업도 하지 않기)

	10. GUI 폼 개발 및 핸들링
	11. CLI, GUI 버전 2가지로 개발하기
"""
import queue
import threading

"""
	1. Fox2Av 는 백신을 구동하기 위한 첫번째 로드된 파일로 하자.
		-> 악성코드 DB의 프리로딩
		-> 필요한 변수 및 리스트 만들어주기
		-> 설정 파일 생성 및 관리 등
		-> 또는 설치 관련 내용??
		
	2. Fox2Av에서 사용자가 시스템 스캔을 지시하면, 필요한 내용을 토대로 하여 스캔 엔진들을 실행시키는 느낌으로 가자.
	__
	3. zip 파일, 다른 화장자의 파일들을 검사하는 로직에 대해서 생각이 필요할듯??
	
"""


import os

# import core Libs
from lib.scanlogger import ScanLoggingConfigure

# import plugin engines
from Foxcore.PlugInEngine.Signature import *
from Foxcore.PlugInEngine.zipcheck import *

# Libs for pretty CLI, interface
from FoxInterface.FoxVc_PrettyCLI import *


# global variable
File_Size_List = []
File_Hash_List = []
File_Name_List = []

DB_PATH = "./Foxdb/main.hdb" # maleware DB
memory = 1024 * 100 # 102400

Hash_Matching_List = [] # 해시 매칭 리스트
Value_Matching_List = [] # 추가적인 검사 매칭 리스트

INFECTION = [] # 감염 파일 리스트
zip_INFECTION = []

# set logger
slogger = ScanLoggingConfigure()

def pre_load():
	global File_Name_List
	global File_Size_List
	global File_Hash_List

	# DB를 불러옴.
	with open(DB_PATH, "r") as fdb:
		for hdb in fdb.readlines(memory):  # 지정된 메모리 안에서 DB를 불러옴. >> 정확한 내용은 모르겠으나, DB사이즈가 메모리 범위 밖이여도 상관없는 듯...
			hdb = hdb.split("\n")[0]
			File_Hash_List.append(str(hdb.split(':')[0]))  # DB에서 두번째 부분(파일md5해시)부분만 잘라서 FHL(FileHashList)
			File_Size_List.append(int(hdb.split(':')[1]))  # DB에서 맨 앞부분(파일용량)부분만 잘라서 FSL(FileSizeList)에 추가
			File_Name_List.append(str(hdb.split(':')[2]))  # DB에서 세번째 부분(파일 이름)부분 잘라서 FNL(FileNAmeList)


def get_drives():
	drives = []
	for drive in range(ord('A'), ord('Z') + 1):
		drive_letter = f"{chr(drive)}:\\"
		if os.path.exists(drive_letter):
			drives.append(drive_letter)
	return drives

def req_Targeted_Scan():
	print("")


def FoxVcMain():
	#req_Entire_Scan()
	"""
	global INFECTION, File_Hash_List

	print_FoxVc_Logo()
	pre_load() # preload malware db data

	devider() # wait user's command
	call_datetime_cli("*** FoxVc Scan CLI command-line ***")
	call_cli("waiting user's command..\n")

	Sig_scan(File_Hash_List)

	devider()
	res = Sig_report()
	if res != False:
		Sig_cure()
"""

if __name__ == "__main__":
	FoxVcMain()

	
			
	
