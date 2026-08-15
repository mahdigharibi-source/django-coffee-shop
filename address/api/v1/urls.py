from django.urls import path
from .views import AddressCreateApiView

app_name = 'api-v1'
urlpatterns = [
    path('create/', AddressCreateApiView.as_view(), name='create-api-view'),
]