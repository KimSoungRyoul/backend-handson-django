from django.db import connection
from django.db import connections
from django.test import TestCase

from aggregate.users.models import User
from study_example_app.models import ciphers


class CipherExampleTest(TestCase):
    def test_aes_encrypt_decrypt(self):

        plaintext = "안녕하세요... Hello @#$%^&"
        ciphertext: bytes = ciphers.AES256Cipher.encrypt(plaintext=plaintext)
        print(ciphertext)

        decrypted_data: str = ciphers.AES256Cipher.decrypt(ciphertext=ciphertext)
        print(decrypted_data)

    def test_seed_encrypt_decrypt(self):
        plaintext = "안녕하세요... Hello @#$%^&"
        ciphertext: bytes = ciphers.SEED128Cipher.encrypt(plaintext=plaintext)
        print(ciphertext)
        a = ciphertext.decode("utf-8")

        decrypted_data: str = ciphers.SEED128Cipher.decrypt(ciphertext=a.encode("utf-8"))
        print(decrypted_data)

    def test_user_create(self):
        created_u: User = User.objects.create_user(
            username="userna3me145", password="1234", registration_number="930823-1233456999", name_kor="a" * 64,
        )
        print(created_u.registration_number)

        selected_user = User.objects.get(username="userna3me145")
        print(selected_user.registration_number)
        with connections["default"].cursor() as cursor:
            cursor.execute(
                """SELECT "user"."username",  "user"."registration_number" FROM "user" WHERE username='userna3me145'""",
                [],
            )
            row = cursor.fetchone()

        print("DB에 저장된 registration_number:", row[1])
        print("DB에 저장된 registration_number 직접 복호화:", ciphers.AES256Cipher.decrypt(row[1].encode("utf-8")))
