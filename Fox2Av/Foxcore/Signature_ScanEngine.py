# -*- coding: utf-8 -*-

# Author : github.com/miho030

import hashlib

def Matching_Hash_Value(fname, file_hash_list, file_name_list):
	blacklist = ["bin", "BIN", "$RECYCLE", "$RECYCLE.BIN"]  # 휴지통을 블랙리스트로 넣음

	if fname in blacklist:
		return False

	try:
		with open(fname, 'rb') as f:
			buf = f.read()
			md5 = hashlib.md5()
			md5.update(buf)
		# end file open

		fmd5 = md5.hexdigest()

		for malHash, malName in zip(file_hash_list, file_name_list):
			if fmd5 == malHash:  # 만약 파일의 md5해시가 멀웨어 DB에 존재한다면..
				return True, malHash, malName

		return False, "", ""    # 루프가 끝날 때까지 매칭되지 않으면 False 반환

	except FileNotFoundError:
		print(f"FileNotFoundError : No such file or directory.")

	except IOError as IOe:
		print(f"IOError : {IOe.message}")

	except Exception as e:
		print(f"An unexpected error occurred: {e}")

	finally:
		pass