from django.urls import path
from .views import DashboardAdminView
app_name = 'admin'
urlpatterns = [
    path('home', DashboardAdminView.as_view(), name='home'),
]