from django.contrib import admin

from cart.models import CartItems, Cart

admin.site.register(Cart)
admin.site.register(CartItems)
