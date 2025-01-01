# -*- coding: utf-8 -*-

# Author : github.com/miho030
"""
* engine name : Fox2Av-SIN.engine
* engine type : Plugin/scan
"""

import os

# import core Libs
from Foxcore.Signature_ScanEngine import Matching_Hash_Value

# Libs for pretty CLI, interface
from FoxInterface.FoxVc_PrettyCLI import *

"""
zip 스캔 엔진 등 여러  plugin 엔진에서 시행되는
검사 중, signature 엔진으로는 검사가 힘들다고 판단되는 경우( 또는 중간에 스캔 큐를 넣기 힘들다고 판단되는 경우)
단일 검사 형태로 진행 (마우스 우클릭을 통해서 검사하는 항목에서 이 엔진 사용 가능)

기존 시그니처 엔진은 사용자가 지정한 디렉터리 하위 전체 단위로 작동하며,
그 과정에서 진단 가능한 확장자가 나온 경우에 추가적으로 보내는 것이기 때문에..

(쓰레드 또는 논쓰레드) 기반의 단일 엔진 필요성 있음.
"""

def engineInfo():
    engine_name = "Fox2Av-SIN.engine"
    engine_type = "Plugin/scan"
    engine_ver = "0.0.1"

    return engine_name, engine_type, engine_ver


def scanSingleFile(fname :str, hashlist :list):
    if not Matching_Hash_Value(fname, hashlist) == 1:
        return False
    else:
        return True


def scanFewFiles_list(scanList :list, hashlist :list):
    scanResList = []

    for fname in scanList:
        if not Matching_Hash_Value(fname, hashlist) == 1:
            continue
        else:
            scanResList.append(fname)
    return scanResList

def scanFewFiles_dict(zip_dict :dict, hashlist :list):
    zip_scanRes = {}
    infected_fileList = []

    # 딕셔너리 순회하면서 함수 호출
    for zip_file, file_list in zip_dict.items():
        for fname in file_list:
            if not Matching_Hash_Value(fname, hashlist) == 1:
                continue
            else:
                infected_fileList.append(fname)
            zip_scanRes[zip_file] = infected_fileList

    return zip_scanRes