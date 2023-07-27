from users.models import ReservePhoneNumber, User, Verification
from rest_framework.test import APITestCase


class AuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', phone_number='+99361000001')
        ReservePhoneNumber.objects.create(user=self.user, phone_number='+99361000000')

    def test_sign_up_success(self):
        # Test Sign-Up
        response = self.client.post('/api/auth/sign-up', {'phone_number': '+99361945186', }, format='json')
        self.assertEqual(response.status_code, 200)

        # Test Verification with code
        user = User.objects.get(phone_number='+99361945186')
        verification_code = Verification.objects.get(user=user).code
        response = self.client.post('/api/auth/verify', {'phone_number': '+99361945186',
                                                         "verification-code": verification_code})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        refresh_token = response.data['refresh']

        # Test Get User
        response = self.client.get('/api/auth/get-user', HTTP_AUTHORIZATION=f"Bearer {response.data['access']}",
                                   format='json')
        self.assertEqual(response.status_code, 200)

        # Test Refresh Token
        response = self.client.post('/api/token/refresh/', {'refresh_token': refresh_token}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_sign_up_blank(self):
        response = self.client.post('/api/auth/sign-up', {'phone_number': '', })
        self.assertEqual(response.status_code, 403)

    def test_sign_up_invalid(self):
        response = self.client.post('/api/auth/sign-up', {'phone_number': '+99361000000', })
        self.assertEqual(response.status_code, 409)
