from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

app_name = 'accounts-api-v1'
urlpatterns = [
    # User profile management
    path('user', UserInformationApi.as_view(), name='user'),

    # Registration management
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    # path("register/email-verify/", VerifyEmailApiView.as_view(), name="email_verify"),
    # path("register/email-verify/resend/", ResendVerifyEmailApiView.as_view(), name="email_verify"),

    # Password management
    # path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # path("reset-password/", PasswordResetRequestEmailApiView.as_view(), name="reset-password-request"),
    # path("reset-password/validate-token/", PasswordResetTokenValidateApiView.as_view(), name="reset-password-validate"),
    # path("reset-password/set-password/", PasswordResetSetNewApiView.as_view(), name="reset-password-confirm"),

    # Token authentication
    path('token/login/', CustomObtainAuthToken.as_view(), name='token-login-view'),
    path('token/logout/', ApiLogoutTokenView.as_view(), name='token-logout-view'),

    # JWT authentication
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

]