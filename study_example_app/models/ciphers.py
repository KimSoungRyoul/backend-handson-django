from __future__ import annotations

import abc
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes
from django.conf import settings


class ABCCipher(metaclass=abc.ABCMeta):
    _algorithm = None
    _encryption_key: bytes
    _init_vector = b"1616161616161616"

    @classmethod
    @property  # python 3.9부터 classmethod와 property 혼합 사용이 가능합니다.
    def _padding(cls):
        return padding.PKCS7(cls._algorithm.block_size)

    @classmethod
    @property
    def _cipher(cls) -> Cipher:
        return Cipher(
            algorithm=cls._algorithm(key=cls._encryption_key),
            mode=modes.CBC(cls._init_vector),
            backend=default_backend(),
        )

    @classmethod
    def encrypt(cls, plaintext: str) -> bytes:
        encryptor = cls._cipher.encryptor()
        padder = cls._padding.padder()
        padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted_text)

    @classmethod
    def decrypt(cls, ciphertext: bytes) -> str:
        decryptor = cls._cipher.decryptor()
        encrypted = base64.b64decode(ciphertext)
        padded_data = decryptor.update(encrypted) + decryptor.finalize()
        unpadder = cls._padding.unpadder()
        return (unpadder.update(padded_data) + unpadder.finalize()).decode("utf-8")


class AES256Cipher(ABCCipher):
    """
        프로젝트내 Column 암복호화 목적으로 사용
    """

    _algorithm = algorithms.AES
    _encryption_key = settings.AES256_ENCRYPTION_KEY


class SEED128Cipher(ABCCipher):
    """
        한국에서 자체적으로 개발한 암호화알고리즘, 주로 은행,공공기관에서 사용
    """

    _algorithm = algorithms.SEED
    _encryption_key = settings.SEED256_ENCRYPTION_KEY
