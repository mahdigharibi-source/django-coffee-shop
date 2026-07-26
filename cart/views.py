from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from cart.cart import CartSession
from cart.models import Cart, CartItems
from shop.models import Product


class SessionAddProductView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        if not Product.objects.get(id=int(product_id)):
            return JsonResponse({"error": "Product not found"}, status=404)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItems.objects.get_or_create(cart=cart, product_id=product_id, defaults={"quantity": 1})

            if not created:
                cart_item.quantity += 1
                cart_item.save()


            total_quantity = sum(item.quantity for item in cart.items.all())
            return JsonResponse({"total_quantity": total_quantity})

        else:
            cart = CartSession(self.request)
            cart.add_product(product_id)

            return JsonResponse({
                "cart": cart.get_cart_dict(),
                "total_quantity": cart.get_total_quantity()
            })

class SessionRemoveProductView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = Product.objects.filter(id=int(product_id)).exists()
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            CartItems.objects.get(cart=cart, product_id=product_id).delete()

            return JsonResponse({"success": True})

        else:
            cart_session = CartSession(self.request)
            cart_session.remove_product(product_id)

            return JsonResponse({"cart": cart_session.get_cart_dict(), "total_quantity": cart_session.get_total_quantity()})

class SessionUpdateProductView(View):
    def post(self, request, *args, **kwargs):
        cart_session = CartSession(self.request)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        if product_id and quantity:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
                CartItems.objects.get(cart=cart, product_id=product_id).quantity = int(quantity)
                return JsonResponse({"success": True})
            else:
                cart_session.update_product_quantity(product_id, quantity)
                return JsonResponse({"success": True})

        return JsonResponse({"cart": cart_session.get_cart_dict(), "total_quantity": cart_session.get_total_quantity()})

class SessionIncreaseProductView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        if not Product.objects.filter(id=int(product_id)).exists():
            return JsonResponse({"error": "Product not found"}, status=404)

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            item = CartItems.objects.get(cart=cart, product_id=product_id)
            item.quantity += 1
            item.save()

            return JsonResponse({
                "success": True
            })

        else:
            cart_session = CartSession(self.request)
            cart_session.increase_quantity(product_id)

            return JsonResponse({"cart": cart_session.get_cart_dict(), "total_quantity": cart_session.get_total_quantity()})

class SessionDecreaseProductView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        if not Product.objects.filter(id=int(product_id)).exists():
            return JsonResponse({"error": "Product not found"}, status=404)

        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            item = CartItems.objects.get(cart=cart, product_id=product_id)
            item.quantity -= 1
            item.save()

            return JsonResponse({
                "success": True
            })

        else:
            cart_session = CartSession(self.request)
            cart_session.decrease_quantity(product_id)

            return JsonResponse(
                {"cart": cart_session.get_cart_dict(), "total_quantity": cart_session.get_total_quantity()})

class CartSummaryView(TemplateView):
    template_name = 'cart/list-items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request)
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context


