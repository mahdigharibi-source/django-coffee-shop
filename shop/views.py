from itertools import product

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from cart.cart import CartSession
from shop.forms import CommentsForm
from shop.models import Product, ProductStatusType, Favorite, Category


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(
            status=ProductStatusType.PUBLISHED)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
                print('ok')
            except FieldError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['favorite_ids'] = set(
                Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            )
        else:
            context["favorite_ids"] = set()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """
        این متد برای فرستادن داده‌های اضافه به template است.
        خود DetailView به‌صورت پیش‌فرض فقط object را می‌فرستد
        ولی ما می‌خواهیم comments و form و review_stats را هم بفرستیم.
        """
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request)
        product = self.object

        comments = product.comments.all()
        context['comments'] = comments

        for item in cart.get_cart_items():
            if item['product_obj'].id == self.object.id:
                context['quantity'] = item['quantity']

        return context

    def post(self, request, *args, **kwargs):
        """
        وقتی فرم ثبت نظر submit می‌شود، این متد اجرا می‌شود.
        """
        # خیلی مهم:
        # باید آبجکت محصول را دستی بگیریم تا self.object پر شود
        self.object = self.get_object()
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object

            if request.user.is_authenticated:
                comment.user = request.user

            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')

            return redirect('shop:product-detail', slug=self.object.slug)

        # اگر فرم نامعتبر بود، همان صفحه محصول را با خطاها دوباره رندر می‌کنیم
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class AddToFavoriteView(TemplateView):
    template_name = 'shop/product-list.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "login_required": True
            }, status=401)

        else:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            favorite, create = Favorite.objects.get_or_create(user=request.user, product=product)
            if create:
                is_favorite = True
            else:
                favorite.delete()
                is_favorite = False

            return JsonResponse({
                "is_favorite": is_favorite
            })


class FavoriteListView(TemplateView):
    template_name = 'shop/favorite-list.html'
    model = Favorite

    def get_context_data(self, **kwargs):
        context = super(FavoriteListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            favorite_ids = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            context['product_obj'] = Product.objects.filter(id__in=favorite_ids)
            return context
        else:
            return HttpResponseRedirect('login')




