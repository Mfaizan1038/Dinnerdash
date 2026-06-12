from django import forms
from .models import Item, Category

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    item_id = forms.IntegerField(widget=forms.HiddenInput)

class UpdateCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)
    item_id = forms.IntegerField(widget=forms.HiddenInput)
