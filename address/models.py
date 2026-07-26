from django.db import models

from accounts.models import CustomUser


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    zip_code = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.full_name} - {self.city}'

