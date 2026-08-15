from django.urls import path
from .views import AddressCreateApiView, AddressUpdateApiView

app_name = 'api-v1'
urlpatterns = [
    path('create/', AddressCreateApiView.as_view(), name='create-api-view'),
    path('update/<int:pk>/', AddressUpdateApiView.as_view(), name='update-api-view'),
]