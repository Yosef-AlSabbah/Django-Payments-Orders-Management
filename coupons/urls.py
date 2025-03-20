from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'coupons'

urlpatterns = [
    path(_('apply/'), views.coupon_apply, name='apply'),
]
