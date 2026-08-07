from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.api.v1.views import RegistrationApiView, CustomObtainAuthToken

app_name = 'accounts-api-v1'
urlpatterns = [
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    path('token/login/', ObtainAuthToken.as_view(), name='token_obtain_pair'),
]