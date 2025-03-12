from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    if not category_slug:
        products = Product.offered.all()
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.offered.filter(category=category)

    return render(
        request,
        'shop/product/list.html',
        context={
            'categories': categories,
            'category': category,
            'products': products,
        }
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, available=True, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/detail.html',
        context={
            'product': product,
            'cart_product_form': cart_product_form,
        }
    )
