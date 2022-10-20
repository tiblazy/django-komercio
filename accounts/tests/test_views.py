from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import Account

from .mock import (mock_admin, mock_seller, mock_buyer,mock_seller_update_info, mock_seller_cant_update_info, mock_login_seller, mock_login_buyer,)

class AccountViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_mock_admin = mock_admin
        cls.account_mock_seller = mock_seller
        cls.account_mock_buyer = mock_buyer
        cls.account_mock_seller_update_info = mock_seller_update_info
        cls.account_mock_seller_cant_update_info = mock_seller_cant_update_info
        
        cls.account_seller = Account(**cls.account_mock_seller)
        cls.account_buyer = Account(**cls.account_mock_buyer)

        cls.account_login_seller_one = mock_login_seller
        cls.account_login_buyer = mock_login_buyer
        
        cls.account_admin = Account.objects.create_superuser(**cls.account_mock_admin)        
        cls.account_admin_token = Token.objects.create(user=cls.account_admin)

        cls.account_seller_to_update = Account.objects.create_user(**cls.account_mock_seller_update_info)        
        cls.account_seller_to_update_token = Token.objects.create(user=cls.account_seller_to_update)
        cls.account_seller_cant_update = Account.objects.create_user(**cls.account_mock_seller_cant_update_info)        
        cls.account_seller_cant_update_token = Token.objects.create(user=cls.account_seller_cant_update)
        
        cls.base_url = reverse('accounts')
        cls.base_url_login = reverse('login')
        cls.base_url_patch = reverse('accounts_updated', args=[cls.account_seller_to_update.id])        
        cls.base_url_patch_admin = reverse('accounts_updated_admin', args=[cls.account_seller_to_update.id])
        
    def test_can_create_seller(self):
        response = self.client.post(self.base_url, self.account_mock_seller, format='json')
        
        data = {
            "username": self.account_mock_seller['username'],
            "first_name": self.account_mock_seller['first_name'],
            "last_name": self.account_mock_seller['last_name'],
            "is_superuser": False,
            "is_active": True,
            "is_seller": self.account_mock_seller['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)
        
    def test_can_create_buyer(self):
        response = self.client.post(self.base_url, self.account_mock_buyer, format='json')
        
        data = {
            "username": self.account_mock_buyer['username'],
            "first_name": self.account_mock_buyer['first_name'],
            "last_name": self.account_mock_buyer['last_name'],
            "is_superuser": False,
            "is_active": True,
            "is_seller": self.account_mock_buyer['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)
        
    def test_cant_create_seller_with_wrong_keys(self):
        response = self.client.post(self.base_url, {}, format='json')
        
        data = {
            "username": ["This field is required."],
            "password": ["This field is required."],
            "first_name": ["This field is required."],
            "last_name": ["This field is required."],
            "is_seller": ["This field is required."]
        }
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)
                
    def test_cant_create_buyer_with_wrong_keys(self):
        response = self.client.post(self.base_url, {}, format='json')
        
        data = {
            "username": ["This field is required."],
            "password": ["This field is required."],
            "first_name": ["This field is required."],
            "last_name": ["This field is required."],
            "is_seller": ["This field is required."]
        }
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)
        
    def test_can_login_seller(self):
        self.client.post(self.base_url, self.account_mock_seller, format='json')
        response = self.client.post(self.base_url_login, self.account_login_seller_one, format='json')

        data = {
            "token": response.data['token']
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)
        
    def test_can_login_buyer(self):
        self.client.post(self.base_url, self.account_mock_buyer, format='json')
        response = self.client.post(self.base_url_login, self.account_login_buyer, format='json')

        data = {
            "token": response.data['token']
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)
        
    def test_can_update_same_user_info_and_cant_change_is_active(self):
        updated_info = {
            "is_active": False,
            "first_name": "Updated"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller_to_update_token.key)
        response = self.client.patch(self.base_url_patch, updated_info, format='json')
                
        data = {
            "username": self.account_mock_seller_update_info['username'],
            "first_name": "Updated",
            "last_name": self.account_mock_seller_update_info['last_name'],
            "is_superuser": False,
            "is_active": True,
            "is_seller": self.account_mock_seller_update_info['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)
        
    def test_cant_update_other_user_info(self):
        updated_info = {
            "is_active": False,
            "first_name": "Updated"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller_cant_update_token.key)
        response = self.client.patch(self.base_url_patch, updated_info, format='json')
        
        data = {
	        "detail": "You do not have permission to perform this action."
        }
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)
        
    def test_admin_can_change_is_active_to_false(self):
        update_info = {
            "is_active": False
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_admin_token.key)
        response = self.client.patch(self.base_url_patch_admin, update_info, format='json')
        
        data = {
            "username": self.account_mock_seller_update_info['username'],
            "first_name": self.account_mock_seller_update_info['first_name'],
            "last_name": self.account_mock_seller_update_info['last_name'],
            "is_superuser": False,
            "is_active": False,
            "is_seller": self.account_mock_seller_update_info['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)
        
    def test_admin_can_change_is_active_to_true(self):
        update_info = {
            "is_active": False
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_admin_token.key)
        self.client.patch(self.base_url_patch_admin, update_info, format='json')
        
        update_info = {
            'is_active': True
        }
        
        response = self.client.patch(self.base_url_patch_admin, update_info, format='json')
        
        data = {
            "username": self.account_mock_seller_update_info['username'],
            "first_name": self.account_mock_seller_update_info['first_name'],
            "last_name": self.account_mock_seller_update_info['last_name'],
            "is_superuser": False,
            "is_active": True,
            "is_seller": self.account_mock_seller_update_info['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)
        
    def test_can_anyone_list_accounts(self):
        response = self.client.get(self.base_url, format='json')
        
        self.assertEqual(response.status_code, 200)