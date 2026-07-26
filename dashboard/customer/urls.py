from django.urls import path
from .views import DashboardCustomerView
app_name = 'customer'
urlpatterns = [
    path('home', DashboardCustomerView.as_view(), name='home'),
]