from django.contrib.auth.password_validation import password_changed
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
# from django.contrib.auth.urls import
from django.urls import path, include, re_path
from .views import ProfileUpdateView, RegisterView, ProfileDetailView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    path('api/v1/', include('accounts.api.v1.urls')),

    # djoser
    path('api/v2', include('djoser.urls')),
    path('api/v2', include('djoser.urls.jwt')),
]