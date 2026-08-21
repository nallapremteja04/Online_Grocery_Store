from django.test import TestCase, Client
from django.urls import reverse
from ogs.models import Category, Product

class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fresh Fruits")
        self.product = Product.objects.create(
            name="Organic Apple",
            category=self.category,
            price=120.00,
            stock=25,
            available=True
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), "Fresh Fruits")

    def test_product_creation(self):
        self.assertEqual(str(self.product), "Organic Apple")
        self.assertEqual(self.product.price, 120.00)
        self.assertTrue(self.product.available)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Beverages")
        self.product = Product.objects.create(
            name="Orange Juice",
            category=self.category,
            price=80.00,
            stock=10,
            available=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_products_page(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

