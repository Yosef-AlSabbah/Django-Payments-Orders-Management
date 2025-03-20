from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        max_length=50,
        label=_('Coupon'),
    )
