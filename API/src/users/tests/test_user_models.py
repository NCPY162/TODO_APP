from rest_framework.test import APITestCase
from users.models import User

class UserTest(APITestCase):
    def test_create_user(self):
        self.user = User.objects.create(
            username="test1",
            firstname="test",
            lastname="test",
            email="test@test.com",
            password="test_1",
            address= "test",
            zipcode= 12345,
            city= "test",
            country= "test"
        )

        self.assertEqual(self.user.username, "test1")
        self.assertEqual(self.user.lastname, "test")
        self.assertEqual(self.user.firstname, "test")
        self.assertEqual(self.user.email, "test@test.com")
        self.assertEqual(self.user.password, "test_1")
        self.assertEqual(self.user.address, "test")
        self.assertEqual(self.user.zipcode, 12345)
        self.assertEqual(self.user.city, "test")
        self.assertEqual(self.user.country, "test")
        

    