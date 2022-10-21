from django.test import TestCase

from accounts.models import Account

from .mock import mock_seller, mock_buyer

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_data = mock_seller
        cls.buyer_data = mock_buyer
        
        cls.seller = Account.objects.create_user(**cls.seller_data)
        cls.buyer = Account.objects.create_user(**cls.buyer_data)

    def test_account_model_seller(self):
        account = Account.objects.get(username='seller_username')        
        
        username_unique = account._meta.get_field('username').unique
        first_name = account._meta.get_field('first_name')
        last_name = account._meta.get_field('last_name')
        
        self.assertIsInstance(account, Account)
        self.assertEqual(account, self.seller)
        
        self.assertTrue(username_unique)        
        
        self.assertEqual(first_name.max_length, 50)
        self.assertFalse(first_name.blank)
        self.assertFalse(first_name.null)
        self.assertFalse(first_name.unique)
        
        self.assertEqual(last_name.max_length, 50)
        self.assertFalse(last_name.blank)
        self.assertFalse(last_name.null)
        self.assertFalse(last_name.unique)
        
        self.assertTrue(account.is_seller)
        
    def test_account_model_buyer(self):
        account = Account.objects.get(username='buyer_username')        
        
        username_unique = account._meta.get_field('username').unique
        first_name = account._meta.get_field('first_name')
        last_name = account._meta.get_field('last_name')
        
        self.assertIsInstance(account, Account)
        self.assertEqual(account, self.buyer)
        
        self.assertTrue(username_unique)        
        
        self.assertEqual(first_name.max_length, 50)
        self.assertFalse(first_name.blank)
        self.assertFalse(first_name.null)
        self.assertFalse(first_name.unique)
        
        self.assertEqual(last_name.max_length, 50)
        self.assertFalse(last_name.blank)
        self.assertFalse(last_name.null)
        self.assertFalse(last_name.unique)
        
        self.assertFalse(account.is_seller)