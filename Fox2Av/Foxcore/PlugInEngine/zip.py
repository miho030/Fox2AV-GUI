# -*- coding: utf-8 -*-

# Author : github.com/miho030
"""
* engine name : Fox2Av-ZIP.engine
* engine type : Plugin/scan
"""

import os, zipfile

# import some core engines and plugins
from Fox2Av.Foxcore.checkSysDir_Engine import *
from Fox2Av.Foxcore.PlugInEngine.Signature import *

# global variables

def getcwdInfo():
	return os.getcwd()

def engineInfo():
    engine_name = "Fox2Av-ZIP.engine"
    engine_type = "Plugin/scan"
    engine_ver = "0.0.1"

    return engine_name, engine_type, engine_ver
"""
    ToDo List
        *. 검사 프로세스는 아래와 같다.
            1. zip 파일 내부 확인 -> 
            2. 검사 리스트 만들기(압축파일명, 압축파일내 파일들)
            3. zip파일별 압축 해제후 해당 파일들을 단일 검사 함수(새로 만들어야함)로 전송한다.
            4. 
        
            
        2. get_info_from_zipfile은 리스트가 아닌 단일 zip 파일을 대상으로?
"""

"""
    zip_file_scan_list = 
    {
        "zipfilePath" : [1.txt, 2.txt, 3.txt]
        "zipfilePath2" : [11.txt, 22.txt, 33.txt]
        ...
    }
    
    위와 같은 형태로 만들어야 한다..
    이렇게 해야 검사를 위해 압축해제 하고, 검사 이후에 편리하게 다시 압축 가능
    
"""

def get_info_from_zipFile(zlist :list):
    zip_contents = {}

    for zip_file in zlist:
        inter_fPath = zip_file
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                encodeList = []
                for file in zip_ref.namelist():
                    file = file.encode('cp437').decode('euc-kr')
                    nfile = str(inter_fPath).replace('.zip', '') + "\\" + file

                    encodeList.append(nfile)
                zip_contents[zip_file] = encodeList

        except zipfile.BadZipFile:
            print(f"Error: '{zip_file}' is not a valid zip file.")
        except FileNotFoundError:
            print(f"Error: '{zip_file}' not found.")

    return zip_contents


def unziper(zip_file_path, extract_to_dir):
    # unarchive target zip file
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                # 한글 인코딩 깨지는 것 방지
                member.filename = member.filename.encode('cp437').decode('euc-kr')
                zip_ref.extract(member, extract_to_dir)

    except zipfile.BadZipFile:
        print(f"Error: '{zip_file_path}' is not a valid zip file.")

    except FileNotFoundError:
        print(f"Error: '{zip_file_path}' not found.")

    except Exception as e:
        print(f"Error! An unexpected error occurred.: {e}")


def unzipHandler(zdict :dict):
    cwd = getcwdInfo()
    archiveTempDir = cwd + "/temp"

    tempUnzipDirList = [] # temp 디렉터리에 압축 해제된 디렉터리 경로 모음 리스트

    try:
        # make temporary directory for unarchive zip file
        os.makedirs(archiveTempDir, exist_ok=True)

        # make directorys for zip files
        for zip_file, file_list in zdict.items():

            # temp 디렉터리에 해당 압축파일들을 해제할 경우
            zipfPath = os.path.splitext(zip_file)[0]
            dirname = os.path.basename(os.path.normpath(zipfPath)) # 해당 압축파일들의 이름만 추출

            tempUnzipDir = archiveTempDir + "\\" + dirname # 엔진의 temp 디렉터리 + 압축파일 폴더명
            os.makedirs(tempUnzipDir, exist_ok=True)
            unziper(zip_file, tempUnzipDir)
            tempUnzipDirList.append(tempUnzipDir)

    except OSError as e:
        call_datetime_cli(f"Error: Failed to create temp directory at '{archiveTempDir}' {e}")

    return tempUnzipDirList


def scanZipContents():
    # ToDo
    #   1. 디렉터리 존재 유무 확인 (Temp 디렉터리에 압축해제된 것들)
    #   2. 디렉터리 존재할 경우, Temp 디렉터리에 있는 파일들을 대상으로 검사 진행
    print("")



def scanZipFile(scanZipList :list, hashlist :list):

    scan_zip_list = get_info_from_zipFile(scanZipList)
    unzipHandler(scan_zip_list)



    # ToDo
    #   압축파일 temp 디렉터리에 잘 저장되게 했으니 검사 로직 추가해야함.
    #       1. 압축 파일들 검사
    #       2. 악성 판단 시, 해당 파일만 리스트로 반환하고, 해당 파일 삭제
    #       3. 원본 압축 파일을 삭제, 악성 파일이 삭제된 압축 파일을 다시 원래 경로에 덮어씌우기
    #       4. 악성 파일이 아닌 압축파일의 경우, 모든 프로세스 종료 후, temp 디렉터리에 모든 내용 지우기


    # ToDo
    #   1. 악성파일 판단 로직 생성 및 정상 파일로 복구 기능 구현
    #   2. 악성파일 판단 로직 세부화 (scanFewFiles_dict)


# res = scanFewFiles_dict(scan_zip_list, hashlist)