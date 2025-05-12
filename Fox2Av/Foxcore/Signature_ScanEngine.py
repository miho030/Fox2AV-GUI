# -*- coding: utf-8 -*-
# Author : github.com/miho030

import os, hashlib


def Matching_Hash_Value(fname, file_hash_list, file_name_list, chunk_size=1024 * 1024 * 10):
	"""
    파일의 MD5 해시를 계산하고, 악성코드 데이터베이스의 해시 목록과 비교합니다.

    :param fname: 검사할 파일의 경로
    :param file_hash_list: 악성코드 데이터베이스의 MD5 해시 목록
    :param file_name_list: 악성코드 파일 이름 목록
    :param chunk_size: 파일을 청크 단위로 읽을 때의 크기 (기본 10MB)
    :return: (악성 여부, 악성 해시, 악성 파일 이름)
    """
	try:
		md5 = hashlib.md5()
		file_size = os.path.getsize(fname)

		with open(fname, 'rb') as f:
			if file_size < 100 * 1024 * 1024:  # 100MB 미만 파일은 전체를 메모리에 로드
				md5.update(f.read())
			else:  # 100MB 이상 파일은 청크 단위로 로드
				while chunk := f.read(chunk_size):
					md5.update(chunk)

		fmd5 = md5.hexdigest()

		for malHash, malName in zip(file_hash_list, file_name_list):
			if fmd5 == malHash:  # 파일의 MD5 해시가 악성코드 DB에 존재하면
				return True, malHash, malName

		return False, fmd5, fname  # 매칭되지 않으면 False 반환

	except FileNotFoundError:
		print(f"FileNotFoundError : No such file or directory - {fname}")

	except IOError as IOe:
		print(f"IOError : {str(IOe)}")

	except Exception as e:
		print(f"An unexpected error occurred: {e}")

	return False, "", ""  # 예외 발생 시 안전하게 False 반환
