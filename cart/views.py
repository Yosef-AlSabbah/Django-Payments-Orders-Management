from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from coupons.froms import CouponApplyForm
from shop.models import Product
from shop.recommender import Recommender
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    form = CartAddProductForm(request.POST)
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            }
        )
    cart_products = [item['product'] for item in cart]
    if cart_products:
        r = Recommender()
        recommended_products = r.suggest_products_for(cart_products, 4)
    else:
        recommended_products = []
    coupon_apply_form = CouponApplyForm()
    return render(
        request,
        'cart/detail.html',
        context={
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products
        }
    )
