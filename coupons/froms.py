from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=50)