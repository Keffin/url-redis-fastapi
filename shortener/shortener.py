import hashlib
import base58


def sha256cov(inputstr: str) -> bytes:
    algo = hashlib.sha256()
    algo.update(inputstr.encode())
    return algo.digest()


def baseEncoded(byteinput: bytes) -> str:
    encoded: bytes = base58.b58encode(byteinput)
    return encoded.decode()


def createShortLink(originalurl: str) -> str:
    url_hash_bytes: bytes = sha256cov(originalurl)
    random_num: int = int.from_bytes(url_hash_bytes, byteorder="big")
    end_result_str: str = base58.b58encode(bytes(str(random_num), "utf-8")).decode()
    return end_result_str[:8]
