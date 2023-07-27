from users.models import ReservePhoneNumber, User, Verification
from rest_framework.test import APITestCase


class AuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', phone_number='+99361000000')
        ReservePhoneNumber.objects.create(user=self.user, phone_number='+99361000000')

    def test_sign_up_success(self):
        response = self.client.post('/api/auth/sign-up', {'phone_number': '+99361945186', }, format='json')
        self.assertEqual(response.status_code, 200)

        verification_code = Verification.objects.get(user=self.user).code
        response = self.client.post('/api/auth/verify', {'phone_number': '+99361945186',
                                                         "verification_code": verification_code})
        self.assertEqual(response.status_code, 200)

    def test_sign_up_blank(self):
        response = self.client.post('/api/auth/sign-up', {'phone_number': '', })
        self.assertEqual(response.status_code, 403)

    def test_sign_up_invalid(self):
        response = self.client.post('/api/auth/sign-up', {'phone_number': '+993610000000', })
        self.assertEqual(response.status_code, 409)
