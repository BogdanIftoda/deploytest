import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

ADMIN = "A"
SELLER = "S"
CUSTOMER = "C"


class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)


class User(AbstractUser):
    ROLES = {
        ADMIN: "Admin",
        SELLER: "Seller",
        CUSTOMER: "Customer",
    }
    role = models.CharField(max_length=1, choices=ROLES, null=True, blank=True, default=CUSTOMER)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class ActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="activation_token")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < now() - timedelta(days=1)  # Expires in 24 hours
