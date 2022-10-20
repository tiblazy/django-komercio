from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import Account
from accounts.tests.mock import (mock_seller, mock_buyer, mock_seller_update_info)

from products.models import Product
from .mock import mock_product, mock_product_to_update, mock_product_negative


class ProductViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        cls.account_mock_seller = mock_seller
        cls.account_mock_seller_not_owner = mock_seller_update_info
        cls.account_mock_buyer = mock_buyer
        
        cls.product_mock = mock_product
        cls.product_mock_to_update = mock_product_to_update
        cls.product_mock_negative = mock_product_negative
        
        cls.account_seller = Account.objects.create_user(**cls.account_mock_seller)        
        cls.account_seller_token = Token.objects.create(user=cls.account_seller)
        cls.account_seller_not_owner = Account.objects.create_user(**cls.account_mock_seller_not_owner)        
        cls.account_seller__not_owner_token = Token.objects.create(user=cls.account_seller_not_owner)
        cls.account_buyer = Account.objects.create_user(**cls.account_mock_buyer)        
        cls.account_buyer_token = Token.objects.create(user=cls.account_buyer)
        
        cls.product_to_update = Product.objects.create(**cls.product_mock_to_update, seller=cls.account_seller)
        
        cls.base_url = reverse('products')
        cls.base_url_patch = reverse('products_update', args=[cls.product_to_update.id])
        
    def test_can_seller_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller_token.key)
        response = self.client.post(self.base_url, self.product_mock)
        
        data = {
            "id": response.data['id'],
            "seller": response.data['seller'],
            "description": self.product_mock["description"],
            "price": response.data['price'],
            "quantity": self.product_mock["quantity"],
            "is_active": response.data["is_active"]
        }
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)
        
    def test_cant_buyer_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_buyer_token.key)
        response = self.client.post(self.base_url, self.product_mock)
        
        data = {
            "detail": "You do not have permission to perform this action."
        }
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)
        
    def test_can_seller_owner_update_product(self):
        update_product = {
            "price": 10.00,
            "quantity": 2
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller_token.key)
        response = self.client.patch(self.base_url_patch, update_product)
        
        data = {
            "id": response.data['id'],
            "seller": response.data['seller'],
            "description": self.product_mock_to_update['description'],
            "price": response.data['price'],
            "quantity": response.data['quantity'],
            "is_active": response.data['is_active']
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_cant_seller_without_owner_update_product(self):
        update_product = {
            "price": 10.00,
            "quantity": 2
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller__not_owner_token.key)
        response = self.client.patch(self.base_url_patch, update_product)
        
        data = {
            "detail": "You do not have permission to perform this action."
        }
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, data)

    def test_can_anyone_list_products(self):
        response = self.client.get(self.base_url, format='json')
        
        self.assertEqual(response.status_code, 200)
        
    def test_can_anyone_filter_a_product(self):
        response = self.client.get(self.base_url_patch, format='json')
        
        self.assertEqual(response.status_code, 200)
        
    def test_cant_create_product_with_wrong_keys(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller_token.key)
        response = self.client.post(self.base_url, {}, format='json')
        
        data = {
            "description": ["This field is required."],
            "price": ["This field is required."],
            "quantity": ["This field is required."]
        }
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)
        
    def test_cant_create_product_with_negative_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.account_seller_token.key)
        response = self.client.post(self.base_url, self.product_mock_negative)

        data = {
            "quantity": ["Ensure this value is greater than or equal to 0."]
        }
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, data)