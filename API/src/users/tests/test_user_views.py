from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.urls import reverse
from unittest import mock
from users.models import User

class CreateUserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test1",
            firstname="test",
            lastname="test",
            email="test@test.com",
            password=make_password("test_1"),
            address= "test",
            zipcode= 12345,
            city= "test",
            country= "test"
        )

        self.url = reverse("user")
        response = self.client.post(reverse("obtain_token"), {
            "username":"test1",
            "password": "test_1"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access_token"]
    
    def test_create_user(self):
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

        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Utilisateur créé avec succès")
    
    def test_create_user_with_noData(self):
        new_user = {}

        response = self.client.post(self.url, new_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Aucune donnée reçue")


    def test_create_existingUser(self):
        self.test_create_user()
        new_user = {
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

        response = self.client.post(self.url, new_user)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["message"], "Cet utilisateur existe déjà en base")

    def test_create_user_with_invalidData(self):
        new_user = {
            "username":"test2",
            "firstname":"test",
            "lastname":"test",
            "email":"test@test.com",
            "password":"test2",
            "address": "test",
            "zipcode": 12345,
            "city": "test",
            "country": "test"
        }

        response = self.client.post(self.url, new_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Echec de création de l'utilisateur")

    @mock.patch("users.views.UserSerializer.save")
    def test_internal_server_error(self, mock_save):
        
        mock_save.side_effect = Exception("Erreur de test")

        user_data = {
            "username":"test3",
            "firstname":"test",
            "lastname":"test",
            "email":"test@test.com",
            "password":"test_2",
            "address": "test",
            "zipcode": 12345,
            "city": "test",
            "country": "test"
        }

        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "Une erreur est survenue")
        self.assertIn("Erreur de test", response.data["errors"])

class GetAllUsersViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test1",
            firstname="test",
            lastname="test",
            email="test@test.com",
            password=make_password("test_1"),
            address= "test",
            zipcode= 12345,
            city= "test",
            country= "test"
        )

        response = self.client.post(reverse("obtain_token"), {
            "username":"test1",
            "password":"test_1"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access_token"]
        self.url = reverse("users")
    
    def test_get_users(self):
        response = self.client.get(self.url, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Les données utilisateur ont été récupérées avec succès")
    
    def test_get_empty_users_data(self):
        with mock.patch("users.models.User.objects.all") as mock_all:
            mock_all.return_value.exists.return_value = False  # simule une base vide
            response = self.client.get(self.url, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data["message"], "Aucune donnée utilisateur trouvée en base")

    def test_get_one_user(self):
        url = reverse("one_user", kwargs={"user_id": self.user.user_id})
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Donnée utilisateur récupérée avec succès")
    
    def test_get_not_existing_user(self):
        url = reverse("one_user", kwargs={"user_id": 10})
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "L'utilisateur demandée n'existe pas en base")
    
    @mock.patch("users.models.User.objects.all")
    def test_internal_server_error(self, mock_all):
        mock_all.side_effect = Exception("Erreur de test lors de la récupération des données")
        response = self.client.get(self.url, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "Une erreur est survenue")
        self.assertIn("Erreur de test lors de la récupération des données", response.data["errors"])

class UpdateUserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
        username="test1",
        firstname="test",
        lastname="test",
        email="test@test.com",
        password=make_password("test_1"),
        address= "test",
        zipcode= 12345,
        city= "test",
        country= "test"
        )

        response = self.client.post(reverse("obtain_token"), {
            "username":"test1",
            "password":"test_1"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access_token"]
    
    def test_update_user(self):
        url = reverse("update_user", kwargs={"user_id":self.user.user_id})
        user = {
            "username":"new_test"
        }
        response = self.client.put(url, user, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Donnée utilisateur mise à jour avec succès")

    def test_update_with_invalid_user_data(self):
        url = reverse("update_user", kwargs={"user_id":self.user.user_id})
        user = {
            "password":"new_pass"
        }
        response = self.client.put(url, user, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Echec de mise à jour de l'utilisateur")
    
    def test_update_not_existing_user(self):
        url = reverse("update_user", kwargs={"user_id": 10})
        user = {
            "username":"new_test"
        }
        response = self.client.put(url, user, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "La donnée utilisateur à mettre à jour n'existe pas en base")

    @mock.patch("users.models.User.objects.get")
    def test_internal_server(self, mock_update):
        mock_update.side_effect = Exception("Erreur de test pour la mise à jour de la donnée")
        url = reverse("update_user", kwargs={"user_id":self.user.user_id})
        user_data = {
            "username": "test_name"
        }

        response = self.client.put(url, user_data, format="json", HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "Une erreur est survenue")
        self.assertIn("Erreur de test pour la mise à jour de la donnée", response.data["errors"])

class DeleteUserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
        username="test1",
        firstname="test",
        lastname="test",
        email="test@test.com",
        password=make_password("test_1"),
        address= "test",
        zipcode= 12345,
        city= "test",
        country= "test"
        )

        response = self.client.post(reverse("obtain_token"), {
            "username":"test1",
            "password":"test_1"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access_token"]
    
    def test_delete_user(self):
        user = User.objects.create(
        username="test2",
        firstname="test",
        lastname="test",
        email="test@test.com",
        password=make_password("test_2"),
        address= "test",
        zipcode= 12345,
        city= "test",
        country= "test"
        )
        url = reverse("delete_user", kwargs={"user_id": user.user_id})
        response = self.client.delete(url, HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Donnée utilisateur supprimée avec succès")
    
    def test_delete_not_existing_user(self):
        url = reverse("delete_user", kwargs={"user_id": 35})
        response = self.client.delete(url, HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "La donnée utilisateur à supprimer n'existe pas")
    
    @mock.patch("users.models.User.objects.get")
    def test_internal_server(self, mock_delete):
        user = User.objects.create(
        username="test5",
        firstname="test",
        lastname="test",
        email="test@test.com",
        password=make_password("test_5"),
        address= "test",
        zipcode= 12345,
        city= "test",
        country= "test"
        )
        mock_delete.side_effect = Exception("Erreur test pour la suppression de donnée")

        url = reverse("delete_user", kwargs={"user_id": user.user_id})

        response = self.client.delete(url, HTTP_AUTHORIZATION = f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "Une erreur est survenue")
        self.assertIn("Erreur test pour la suppression de donnée", response.data["errors"])
