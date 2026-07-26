from django.urls import path
from .views import SessionAddProductView ,SessionRemoveProductView, SessionUpdateProductView, CartSummaryView, SessionIncreaseProductView, SessionDecreaseProductView

app_name = 'cart'
urlpatterns = [
    path("session/add-product/", SessionAddProductView.as_view(), name="session-add-product"),
    path("session/increase-product/", SessionIncreaseProductView.as_view(), name="session-increase-product"),
    path("session/decrease-product/", SessionDecreaseProductView.as_view(), name="session-decrease-product"),

    path("session/remove-product/", SessionRemoveProductView.as_view(), name="session-remove-product"),
    path("session/update-product/", SessionUpdateProductView.as_view(), name="session-update-product"),
    path("summary/", CartSummaryView.as_view(), name="cart-summary"),

]