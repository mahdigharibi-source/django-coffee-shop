from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from accounts.models import CustomUser

class ProductStatusType(models.TextChoices):
    PUBLISHED = 'published', 'نمایش'
    DRAFT = 'draft', 'عدم نمایش'

class CommentsStatusType(models.TextChoices):
    PUBLISHED = 'published', 'نمایش'
    PROCESS = 'process', 'درحال بررسی'
    DRAFT = 'draft', 'عدم نمایش'

class Category(models.Model):
    title = models.CharField(max_length=200, default="coffee")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    title = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True, blank=True)
    image = models.ImageField(default='public/images/products/p1.png', upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    brief_description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=ProductStatusType.choices , default=ProductStatusType.DRAFT)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #comments
    #items

    @property
    def discount_amount(self):
        return (self.price * self.discount_percent) / Decimal('100')

    @property
    def final_price(self):
        return self.price - self.discount_amount

    def is_discounted(self):
        return self.discount_percent > 0

    def is_published(self):
        return self.status == ProductStatusType.PUBLISHED

    def is_in_stock(self):
        return self.stock > 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=550)
    status = models.CharField(max_length=10 ,choices=CommentsStatusType.choices ,default=CommentsStatusType.PROCESS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'product'],
                name="unique_user_product_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.product}"