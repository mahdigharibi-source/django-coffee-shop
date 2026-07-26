
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # لیست سفارش‌های کاربر (یا همه برای ادمین)
    path('list', views.OrderListView.as_view(), name='order_list'),

    # جزئیات یک سفارش
    # path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    #
    # # ایجاد سفارش جدید (مثلاً از روی سبد خرید)
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    #
    # # بروزرسانی سفارش (اضافه/کم کردن آیتم، تغییر وضعیت)
    # path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    #
    # # لغو/حذف سفارش
    # path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
]
