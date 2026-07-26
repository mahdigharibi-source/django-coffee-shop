
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart.cart import CartSession

@receiver(user_logged_in)
def merge_cart(sender, request, user, **kwargs):
    cart = CartSession(request)
    cart.merge_session_cart_in_db(user)
    cart.clear()
