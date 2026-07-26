from django.db import models
from accounts.models import CustomUser
from shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # items

    def __str__(self):
        return self.user.email

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return self.product.title