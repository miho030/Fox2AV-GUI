# -*- coding: utf-8 -*-

# Author : github.com/miho030

#-----------------------------------------------------------------------------------------------------
# DB를 정리하여 루틴에 적용하는 모듈
#-----------------------------------------------------------------------------------------------------
import os

def UnixIsDir(dirInfo :str):
	if os.path.isdir(dirInfo):
		if len(dirInfo) == 1:
			dirS = os.path.abspath(dirInfo)
			return dirS
		else:
			print("It is not Drive or your system doesn't have %s Drive" % (str(dirInfo))) # 존재하지 않는다면 오류문 출력
			return False


def winIsDir(dirInfo :str):
	if len(dirInfo) == 1:
		strDrv = str(dirInfo) + ":\\"  # 윈도우에서 사용하는 경우, 구분자(separator) '\'가 있어야 경로로 인식(e.g C:\\home\\workspace)
		dirS = os.path.abspath(strDrv)
	else:
		dirS = os.path.abspath(dirInfo)

	if os.path.isdir(dirS):
		return dirS
	else:
		print("It is not Drive or your system doesn't have %s Drive" % (str(dirInfo))) # 존재하지 않는다면 오류문 출력
		return False

def isDir(userDirInput :str):
	strOSName = os.name
	if strOSName == 'nt':
		res = winIsDir(userDirInput)
	elif strOSName == 'linux':
		res = UnixIsDir(userDirInput)
	return res