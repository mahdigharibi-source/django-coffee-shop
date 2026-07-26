# cart: {
#     '1': {"quantity": 7, "product_obj": product},
#     '2': {"quantity": 7, "product_obj": product},
# }
from django.db.models import Sum, F
from django.http import JsonResponse

from cart.models import Cart, CartItems
from shop.models import Product

class CartSession:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_product(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
        else:
            self.cart[product_id] = {'quantity': 1}

        self.save()

    def increase_quantity(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease_quantity(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
        self.save()
        return self.cart

    def update_product_quantity(self, product_id, quantity):
        # when we deside inter the value manauly
        if quantity <= 0 :
            raise Exception('quantity must be greater than 0')

        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        self.save()

    def remove_product(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart.pop(product_id)
        self.save()

    def get_cart_dict(self):
        # return cart dictionary
        return self.cart

    def get_cart_items(self):
        # add product_obj and total_price keys to cart for each product
        cart_items = []
        if self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
            except Cart.DoesNotExist:
                return []

            for item in CartItems.objects.filter(cart=cart).select_related('product'):
                cart_items.append({
                    "product_obj": item.product,
                    "quantity": item.quantity,
                    "total_price": item.product.price * item.quantity,
                })
            return cart_items
        else:
            if self.cart:
                product_ids = self.cart.keys()

                products = Product.objects.filter(id__in=product_ids)

                for product in products:
                    quantity = self.cart[str(product.id)]['quantity']
                    cart_items.append({
                        'product_obj': product,
                        'quantity': quantity,
                        'total_price': product.price * quantity,
                    })
                return cart_items

            else:
                return []

    def get_total_quantity(self):
        # for number of cart
        if self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
            except Cart.DoesNotExist:
                return 0
            total = (
                CartItems.objects
                .filter(cart=cart)
                .aggregate(total=Sum("quantity"))
            )
            return total["total"] or 0

        else:
            if self.cart:
                final = 0
                for item in self.cart.values():
                    final += item['quantity']
                return final

            else:
                return 0

    def get_total_payment_amount(self):
        # calculate the all price for cart

        if self.request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=self.request.user)
            except Cart.DoesNotExist:
                return 0

            total = (
                CartItems.objects.filter(
                    cart=cart
                ).aggregate(
                    total=Sum(F("quantity") * F("product__price")))
            )
            return total["total"] or 0

        else:
            if self.cart:
                total = 0
                product_ids = self.cart.keys()
                products = Product.objects.filter(id__in=product_ids)
                for product in products:
                    quantity = self.cart[str(product.id)]['quantity']
                    total += product.price * quantity
                self.save()
                return total

            else:
                return 0

    def clear(self):
        self.session['cart'] = {}
        self.cart = self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True

    def merge_session_cart_in_db(self, user):
        cart, created = Cart.objects.get_or_create(user=user)

        for key, value in self.cart.items():
            print(key, value)
            product_obj = Product.objects.get(id=int(key))
            cart_items, created = CartItems.objects.get_or_create(
                cart=cart,
                product=product_obj,
                defaults={'quantity': value['quantity']}
            )

            if not created:
                cart_items.quantity += value["quantity"]
                cart_items.save()


