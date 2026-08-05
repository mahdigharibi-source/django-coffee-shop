from datetime import date, timedelta
from decimal import Decimal
from random import choices, randint
from string import ascii_uppercase, digits
from django.core.exceptions import ValidationError
from django.db.models import Sum, F
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from address.models import Address
from shop.models import Product


class OrderStatus(models.TextChoices):
    PENDING = "pending", "در انتظار پرداخت"
    PAID = "paid", "پرداخت شده"
    PROCESSING = "processing", "در حال آماده سازی"
    SHIPPED = "shipped", "ارسال شده"
    DELIVERED = "delivered", "تحویل داده شد"
    CANCELED = "canceled", "لغو شده"
    RETURNED = "returned", "مرجوع شده"
    EXPIRED = "expired", "منقضی شده"


def generated_code():
    return ''.join(choices(ascii_uppercase+digits, k=randint(8,10)))


class Discount(models.Model):
    users = models.ManyToManyField(CustomUser, related_name="discounts", blank=True)
    text = models.CharField(default=generated_code, unique=True , max_length=50)
    discount_amount = models.PositiveIntegerField(blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    max_discount_amount = models.PositiveIntegerField(default=150000)
    limit = models.PositiveIntegerField(default=10)
    used_times = models.PositiveIntegerField(default=0)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.discount_amount in [None, ''] and self.discount_percent in [None, '']:
            raise ValidationError(_("you should choose either discount_amount or discount_percent"))
        elif self.discount_amount not in [None, ''] and self.discount_percent not in [None, '']:
            raise ValidationError(_("you should choose one of discount_amount or discount_percent"))

    @property
    def is_expired(self):
        if timezone.now() > self.expiration_date:
            return True
        else:
            return False

    @property
    def is_limited(self):
        if self.used_times >= self.limit:
            return True
        else:
            return False

    @property
    def is_discount_amount(self):
        if self.discount_amount:
            return True
        return False

    @property
    def is_discount_percent(self):
        if self.discount_percent:
            return True
        return False

    def increase_usage(self):
        self.used_times += 1
        self.save(update_fields=["used_times"])

    def calculate_discount(self, total_price):
        discount = 0
        if self.discount_amount is not None:
            discount = self.discount_amount
            return discount
        elif self.discount_percent is not None:
            discount = total_price * self.discount_percent
            if self.max_discount_amount < discount:
                return self.max_discount_amount
            else:
                return discount


    def __str__(self):
        return self.text




class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True, blank=True, related_name="orders")
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    # price before shipping cost and discount amount
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=0, default=100000)

    # price after shipping cost and discount amount
    final_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    is_paid = models.BooleanField(default=False)


    tracking_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # order_items


    class Meta:
        ordering = ['-created_at']

    def calculate_final_price(self):
        discount_amount = 0

        if self.discount:
            discount_amount = self.discount.calculate_discount(self.total_price)

        final_price = self.total_price - discount_amount + self.shipping_cost

        return final_price

    def calculate_total_price(self):
        totals = self.order_items.aggregate(
            total_price=Sum(F("quantity") * F("price")),
        )
        return totals["total_price"] or Decimal("0.00")

    def is_expired(self):
        if timezone.now() - self.created_at > timedelta(minutes=30):
            return True
        return False




class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # price for each item
    @property
    def total_price(self):
        return self.quantity * self.price


#
# @receiver(post_save, sender=OrderItem)
# def update_order_total_on_save(sender, instance, created, **kwargs):
#     instance.order.save()
#
# @receiver(post_delete, sender=OrderItem)
# def update_order_total_on_save(sender, instance, created, **kwargs):
#     instance.order.save()




