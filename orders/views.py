from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # clear the cart
            cart.clear()

            # launch asynchronous task
            order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id

            return redirect('payment:process')

    form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        context={
            'cart': cart,
            'form': form,
        }
    )
