from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, TemplateView

from order.models import Discount, Order, OrderItem


class PaymentView(TemplateView):
    template_name = 'payment/payment.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(user=self.request.user).order_by("-created_at").first()
        return context



    def post(self, request, *args, **kwargs):

        try:
            discount_code = request.POST.get("discount_code")
            discount = Discount.objects.get(text=discount_code)

            order = Order.objects.filter(user=request.user).order_by("-created_at").first()
            order.discount = discount
            order.save()

            return JsonResponse({"status": "success"})

        except Discount.DoesNotExist:
                return JsonResponse({"status": "fail"})