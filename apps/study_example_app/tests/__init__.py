from django.test import TestCase

# Create your tests here.
from aggregate.users.models import User


class DjangoORMExampleTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="abc1234", password="pass1!", email="asdf@naver.com", first_name="김예제")
        User.objects.create_user(username="bbb1234", password="pass1!", email="bbb@naver.com", first_name="최예제")

    def test_example_01(self):
        user_list = User.objects.filter(username="abc1234")
        self.assertEqual(user_list[0].first_name, "김예제")
