from django.urls import path, include
from .views import AddressEditView,AddressCreateView,AddressListView,SetAddressDefault,AddressDeleteView

app_name='address'
urlpatterns = [
    path('list/', AddressListView.as_view(), name='address-list'),
    path('create/', AddressCreateView.as_view(), name='address-create'),
    path('<int:pk>/edit/', AddressEditView.as_view(), name='address-edit'),
    path('delete/', AddressDeleteView.as_view(), name='address-delete'),
    path('set-default/', SetAddressDefault.as_view(), name='set-default'),
    path('api/v1/', include('address.api.v1.urls')),


]