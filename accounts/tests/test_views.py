from django.urls import reverse

from rest_framework.test import APITestCase

from accounts.models import Account

from .mock import mock_seller, mock_buyer

class AccountViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.account_seller = mock_seller
        cls.account_buyer = mock_buyer
        
        cls.account_one = Account(**cls.account_seller)
        cls.account_two = Account(**cls.account_buyer)
        
        cls.base_url = reverse('accounts')
        
    def test_create_seller(self):
        response = self.client.post(self.base_url, self.account_seller)
        
        data = {
            "username": self.account_seller['username'],
            "first_name": self.account_seller['first_name'],
            "last_name": self.account_seller['last_name'],
            "is_superuser": False,
            "is_active": True,
            "is_seller": self.account_seller['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)
        
        
    def test_create_buyer(self):
        response = self.client.post(self.base_url, self.account_buyer)
        
        data = {
            "username": self.account_buyer['username'],
            "first_name": self.account_buyer['first_name'],
            "last_name": self.account_buyer['last_name'],
            "is_superuser": False,
            "is_active": True,
            "is_seller": self.account_buyer['is_seller'],
            "date_joined": response.data['date_joined']
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)