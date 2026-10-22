from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_invalid_email(self):
        url = '/api/auth/register/'
        data = {
            'name': 'Test User',
            'email': 'usuario@gmail.com',
            'password': 'password123',
            'role': 'STUDENT'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_valid_institutional_email(self):
        url = '/api/auth/register/'
        data = {
            'name': 'Andrea Estudiante',
            'email': 'andrea@uniboyaca.edu.co',
            'password': 'password123',
            'role': 'STUDENT'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)