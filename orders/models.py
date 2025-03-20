from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from coupons.models import Coupon


class Order(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('e-mail'), )
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    stripe_id = models.CharField(max_length=250, blank=True)

    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    discount = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(
                fields=['-created']
            )
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount() + self.get_shipping_cost()

    def get_total_weight(self):
        return sum(
            item.get_weight() for item in self.items.all()
        )

    def get_shipping_cost(self):
        total_weight = self.get_total_weight()

        # Define your shipping pricing rules based on weight
        if total_weight <= 1000:  # 1 kg
            return Decimal(5)  # Example: $5 for orders up to 1kg
        elif total_weight <= 5000:  # 5 kg
            return Decimal(10)  # Example: $10 for orders up to 5kg
        else:
            return Decimal(20)  # Example: $20 for orders over 5kg

    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # Stripe path for real payments
            path = '/'

        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.product.weight * self.quantity
