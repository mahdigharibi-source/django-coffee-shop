from django.shortcuts import render
from django.views.generic import TemplateView

from cart.cart import CartSession
from shop.models import Product, Favorite


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        #     context['favorite_ids'] = set(
        #         Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        #     )
        # else:
        #     context["favorite_ids"] = set()
        context['products'] = Product.objects.all()
        return context
