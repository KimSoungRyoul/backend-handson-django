from __future__ import annotations

import base64
import os
from typing import Protocol

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings


class ABCCipher(Protocol):
    _algorithm = None
    _encryption_key: bytes

    @classmethod
    def get_init_vector(cls) -> bytes:
        raise NotImplementedError("암호화 알고리즘과 size에 맞는 난수")

    @classmethod
    @property  # python 3.9부터 classmethod와 property 혼합 사용이 가능합니다.
    def _padding(cls):
        return padding.PKCS7(cls._algorithm.block_size)

    @classmethod
    def _cipher(cls, iv: bytes) -> Cipher:
        return Cipher(
            algorithm=cls._algorithm(key=cls._encryption_key),
            mode=modes.CBC(iv),
            backend=default_backend(),
        )

    @classmethod
    def encrypt(cls, plaintext: str) -> bytes:
        iv = cls.get_init_vector()
        encryptor = cls._cipher(iv=iv).encryptor()
        padder = cls._padding.padder()
        padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted_text + iv)

    @classmethod
    def decrypt(cls, ciphertext: bytes) -> str:
        decoded_str = base64.b64decode(ciphertext)
        iv_len = len(cls.get_init_vector())
        encrypted, iv = decoded_str[:-iv_len], decoded_str[-iv_len:]
        decryptor = cls._cipher(iv=iv).decryptor()
        padded_data = decryptor.update(encrypted) + decryptor.finalize()
        unpadder = cls._padding.unpadder()
        return (unpadder.update(padded_data) + unpadder.finalize()).decode("utf-8")


class AES256Cipher(ABCCipher):
    """
    프로젝트내 Column 암복호화 목적으로 사용
    """

    _algorithm = algorithms.AES256
    _encryption_key = settings.AES256_ENCRYPTION_KEY

    @classmethod
    def get_init_vector(cls) -> bytes:
        return os.urandom(16)


#
# class SEED256Cipher(ABCCipher):
#     """
#     한국에서 자체적으로 개발한 암호화알고리즘, 주로 은행,공공기관에서 사용
#     """
#
#     _algorithm = algorithms.SEED
#     _encryption_key = settings.SEED256_ENCRYPTION_KEY
