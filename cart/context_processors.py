from cart.cart import CartSession
from shop.models import Favorite


def global_variables(request):
    cart = CartSession(request)
    cart_items = cart.get_cart_items()
    product_in_cart = set()
    quantity_in_cart = {}
    for item in cart_items:
        quantity_in_cart[item['product_obj'].id] = item['quantity']
        product_in_cart.add(item['product_obj'].id)
    print(quantity_in_cart)


    return {
        "product_in_cart": product_in_cart,
        "quantity_in_cart": quantity_in_cart,
        "cart_items" : cart_items,
        "total_quantity" : cart.get_total_quantity(),
        "total_payment_price" : cart.get_total_payment_amount()

    }

def global_favorites(request):
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    else:
        favorite_ids = {}

    return {
        "favorite_ids" : favorite_ids,
    }