from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from authentication.models import User
from product.models import Category, Product


# Create your tests here.


class ProductFilterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create Users (Sellers)
        cls.seller1 = User.objects.create_user(username="a", email="seller1@example.com", role="S",
                                               password="testpass")
        cls.seller2 = User.objects.create_user(username="b", email="seller2@example.com", role="S",
                                               password="testpass")

        # Create Categories
        cls.category_electronics = Category.objects.create(name="Electronics")
        cls.category_phones = Category.objects.create(name="Phones", parent=cls.category_electronics)
        cls.category_laptops = Category.objects.create(name="Laptops", parent=cls.category_electronics)

        # Create Products
        cls.product1 = Product.objects.create(
            name="iPhone 14",
            description="Latest Apple phone",
            price=999.99,
            stock=5,
            category=cls.category_phones,
            seller=cls.seller1,
            is_approved=True
        )

        cls.product2 = Product.objects.create(
            name="Samsung Galaxy S22",
            description="Latest Samsung flagship",
            price=899.99,
            stock=10,
            category=cls.category_phones,
            seller=cls.seller1,
            is_approved=True
        )

        cls.product3 = Product.objects.create(
            name="MacBook Pro 16",
            description="Apple laptop with M1 chip",
            price=2499.99,
            stock=2,
            category=cls.category_laptops,
            seller=cls.seller2,
            is_approved=True
        )

        cls.product4 = Product.objects.create(
            name="Dell XPS 15",
            description="High-end Windows laptop",
            price=1799.99,
            stock=0,  # Out of stock
            category=cls.category_laptops,
            seller=cls.seller2,
            is_approved=True
        )

        cls.product5 = Product.objects.create(
            name="Budget Android Phone",
            description="Affordable Android phone",
            price=199.99,
            stock=15,
            category=cls.category_phones,
            seller=cls.seller2,
            is_approved=True
        )

        cls.product6 = Product.objects.create(
            name="Gaming Laptop",
            description="Powerful gaming laptop",
            price=2999.99,
            stock=3,
            category=cls.category_laptops,
            seller=cls.seller1,
            is_approved=True
        )

    def test_filter_category(self):
        response = self.client.get(f"{reverse('product:products-list')}?category=2")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
