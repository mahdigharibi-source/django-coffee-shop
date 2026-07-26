from django.contrib import admin

from shop.models import Product, Comments, Favorite, Category

admin.site.register(Product)
admin.site.register(Comments)
admin.site.register(Favorite)
admin.site.register(Category)
