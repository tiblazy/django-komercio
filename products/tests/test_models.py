from django.test import TestCase

from accounts.tests.mock import mock_seller

from accounts.models import Account

from products.models import Product

from .mock import mock_product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller_data = mock_seller
        cls.seller = Account.objects.create_user(**cls.seller_data)

        cls.product_data = {**mock_product, "seller": cls.seller}
        cls.product = Product.objects.create(**cls.product_data)
        
    def test_product_model(self):
        product = Product.objects.get(description='mock_product')
        
        description = product._meta.get_field('description')
        price = product._meta.get_field('price')
        quantity = product._meta.get_field('quantity')
        is_active = product._meta.get_field('is_active')
        
        self.assertFalse(description.blank)
        self.assertFalse(description.null)
        
        self.assertFalse(price.blank)
        self.assertFalse(price.null)
        self.assertEqual(price.max_digits, 10)
        self.assertEqual(price.decimal_places, 2)
        
        self.assertFalse(quantity.blank)
        self.assertFalse(quantity.null)
        
        self.assertTrue(is_active)
        
        self.assertEqual(product.seller, self.seller)