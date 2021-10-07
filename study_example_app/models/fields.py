import math
from typing import Optional

from django.db.models import CharField
from django.db.models import Field

__all__ = ["EncryptedField", "encrypt_max_length"]

from study_example_app.models import ciphers


def encrypt_max_length(max_length):
    """
    CharField max_length를 DB max_length로 환산한다.
    * AES + PKCS : (plain_text/32 +1) *32
    * base64encoding : 4/3
    """
    return math.ceil(4 * (max_length / 32 + 1) * 32 / 3)


class EncryptedField(CharField):
    _cipher = ciphers.AES256Cipher

    def get_db_prep_save(self, value: str, connection) -> Optional[bytes]:
        value = super().get_db_prep_save(value, connection)
        if value is not None:
            return self._cipher.encrypt(value).decode("utf-8")
        return value

    def from_db_value(self, value, expression, connection, *args) -> Optional[str]:
        return self.to_python(self._cipher.decrypt(value) if value else value)

    def to_python(self, value: str) -> Optional[str]:
        if value is None:
            return value
        return value

    def get_prep_value(self, value: str) -> Optional[bytes]:
        value = super().get_prep_value(value)
        if value is not None:
            return self._cipher.encrypt(value).decode("utf-8")
        return value

    def get_db_prep_value(self, value, connection, prepared=False) -> Optional[str]:
        value = super().get_db_prep_value(value, connection, prepared)
        if not prepared and value is not None:
            return self._cipher.decrypt(value)
        return value


class ValueObjectField(Field):
    ...
