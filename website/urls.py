from website.views import HomePageView
from django.urls import path

app_name = 'website'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]