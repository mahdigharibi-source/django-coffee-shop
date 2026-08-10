from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import *

app_name = 'accounts-api-v1'
urlpatterns = [
    # User profile management
    path('profile/', ProfileApiView.as_view(), name='user'),

    # Registration management
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    # activation
    path('activation/confirm/<str:token>', ActivationApiView().as_view(), name='activate'),
    # resent activation
    path('activation/resend', ActivationResendApiView.as_view(), name='resend'),

    # Password management
    path("change-password/", ChangePasswordApiView.as_view(), name="change-password-api"),
    # for find user
    path("reset-password/", PasswordResetRequestEmailApiView.as_view(), name="reset-password-request"),
    # for test token
    path("reset-password/validate-token/", PasswordResetTokenValidateApiView.as_view(), name="reset-password-validate"),
    # for set password finally
    path("reset-password/set-password/", PasswordResetSetNewApiView.as_view(), name="reset-password-confirm"),

    # Token authentication
    path('token/login/', CustomObtainAuthToken.as_view(), name='token-login-view'),
    path('token/logout/', ApiLogoutTokenView.as_view(), name='token-logout-view'),

    # JWT authentication
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

]