from rest_framework.test import APITestCase

# Create your tests here.


class UserViewSetTest(APITestCase):


    def test_user_list_api(self):

        response  = self.client.get(path="api/users/",data={""})
