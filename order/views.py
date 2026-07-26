from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView
import traceback # این را بالای فایل اضافه کنید
from address.models import Address
from cart.cart import CartSession
from cart.models import CartItems, Cart
from order.models import Order, OrderItem, Discount

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

class OrderListView(TemplateView):
    template_name = 'order/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order__user=self.request.user).select_related("product")
        return context


class OrderCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        try:
            # استفاده از transaction برای اینکه یا همه چیز ذخیره شود یا هیچ چیز
            with transaction.atomic():
                # پیدا کردن امن سبد خرید
                cart = get_object_or_404(Cart, user=request.user)
                cart_items = cart.items.all()
                print(cart_items)

                if not cart_items.exists():
                    return JsonResponse({'status': 'error', 'message': 'سبد خرید خالی است.'}, status=400)

                addresses = Address.objects.filter(user=request.user)
                if not addresses.exists():
                    # return JsonResponse({
                    #     'status': 'error',
                    #     'message': 'لطفا ابتدا یک آدرس انتخاب کنید',
                    #     'redirect_url': reverse('address:address-create')
                    # }, status=400)
                    return redirect('address:address-create')

                else:
                    default_address = Address.objects.get(user=request.user, is_default=True)

                # ایجاد سفارش
                order = Order.objects.create(
                    user=request.user,
                    address=default_address,
                )
                order.status = 'PENDING'

                # ایجاد آیتم های سفارش
                for item in cart_items:

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,  # ذخیره قیمت لحظه‌ای

                    )



                # پاک کردن سبد خرید پس از ثبت موفق
                cart.items.all().delete()
                cart.delete()

                cart_session = CartSession(self.request)
                cart_session.clear()


                order.total_price = order.calculate_total_price()
                order.final_price = order.calculate_final_price()

                if order.is_expired():
                    order.status = 'EXPIRED'

                order.save()
                print(order.final_price)

                return redirect('payment:payment_create')

                # return JsonResponse({
                #     'status': 'success',
                #     'naro' : 'naro',
                #     'redirect_url': reverse('payment:payment_create')
                # })




        except Exception as e:

            # این بخش بسیار مهم است:

            # اگر هر خطایی رخ دهد، متن دقیق خطا را در پاسخِ AJAX می‌فرستد

            error_message = traceback.format_exc()

            print(f"DEBUG ERROR: {error_message}")  # این را در ترمینال چاپ می‌کند

            return JsonResponse({

                'status': 'error',

                'message': str(e),

                'traceback': error_message  # این باعث می‌شود خطا را در مرورگر ببینید

            }, status=500)



