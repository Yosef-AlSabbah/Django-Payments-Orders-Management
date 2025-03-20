from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Product, Category
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    if not category_slug:
        products = Product.objects.all()
    else:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug
        )
        products = Product.objects.filter(category=category)

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
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        available=True,
        id=id,
        translations__language_code=language,
        translations__slug=slug
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        'shop/product/detail.html',
        context={
            'product': product,
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products,
        }
    )
