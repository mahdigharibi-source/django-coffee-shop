
from django.urls import path, include, re_path
from .views import ProductListView, ProductDetailView, AddToFavoriteView, FavoriteListView

app_name = 'shop'
urlpatterns = [
    path('product/grid/', ProductListView.as_view(), name='product_grid'),
    re_path(r'product/(?P<slug>[-\w]+)/detail/', ProductDetailView.as_view(), name='product-detail'),
    path('add/favorite', AddToFavoriteView.as_view(), name='add_favorite'),
    path('favorite/list', FavoriteListView.as_view(), name='favorite_list'),
]