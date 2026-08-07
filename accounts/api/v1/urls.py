from django.urls import path
from .views import *
app_name = 'accounts-api-v1'
urlpatterns = [
    path('registration/', RegistrationApiView.as_view(), name='registration'),
]