from django.urls import path, include

from .views import DashboardHomeView

app_name = 'dashboard'
urlpatterns = [
    path('home', DashboardHomeView.as_view(), name='dashboard-home'),
    path('admin/', include('dashboard.admin.urls')),
    path('customer/', include('dashboard.customer.urls')),
]