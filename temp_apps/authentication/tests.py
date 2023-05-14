# Create your tests here.
from aggregate.users.models import User
from django.contrib.auth import authenticate
from django.test import TestCase


class AuthenticateTestCase(TestCase):
    def test_authenticate(self):
        user = User.objects.create_user(username="soungryoul.kim", password="1234", email="kimsoungryoul@gmail.com")

        logined_user: User = authenticate(username="soungryoul.kim", password="1234")

        self.assertEqual(user, logined_user, msg="authenticate()메서드는 로그인성공시 User를 반환합니다")
