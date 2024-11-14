from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer

class UserSerializerTest(APITestCase):
    def setUp(self):
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
    
    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data

        self.assertEqual(data["username"], "test1")
        self.assertEqual(data["firstname"], "test")
        self.assertEqual(data["lastname"], "test")
        self.assertEqual(data["email"], "test@test.com")
        # self.assertEqual(data["password"], "test_1")
        self.assertEqual(data["address"], "test")
        self.assertEqual(data["zipcode"], 12345)
        self.assertEqual(data["city"], "test")
        self.assertEqual(data["country"], "test")
    
    def test_serializer_with_valid_data(self):
        user_data = {
            "username":"test2",
            "firstname":"test",
            "lastname":"test",
            "email":"test@test.com",
            "password":"test_2",
            "address": "test",
            "zipcode": 12345,
            "city": "test",
            "country": "test"
        }

        serializer = UserSerializer(data=user_data)
        
        self.assertTrue(serializer.is_valid())
        data = serializer.save()

        self.assertEqual(data.username, "test2")
        self.assertEqual(data.firstname, "test")
        self.assertEqual(data.lastname, "test")
        self.assertEqual(data.email, "test@test.com")
        self.assertTrue(data.check_pass("test_2"))
        self.assertEqual(data.address, "test")
        self.assertEqual(data.zipcode, 12345)
        self.assertEqual(data.city, "test")
        self.assertEqual(data.country, "test")
    
    def test_serializer_with_invalid_data(self):
        user_data = {
            "username":"test3",
            "firstname":"test",
            "lastname":"test",
            "email":"test@test.com",
            "password":"test_3",
            "address": "test",
            "zipcode": "un",
            "city": "test",
            "country": "test"
        }

        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("zipcode", serializer.errors)
        
    def test_serializer_with_incomplete_data(self):
        user_data = {
            "firstname":"test",
            "lastname":"test",
            "email":"test@test.com",
            "address": "test",
            "zipcode": 12345,
            "city": "test",
            "country": "test"
        }

        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("password", serializer.errors)

    


        
