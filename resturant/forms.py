from django import forms
from .models import Item, Category

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    item_id = forms.IntegerField(widget=forms.HiddenInput)

class UpdateCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)
    item_id = forms.IntegerField(widget=forms.HiddenInput)

class ItemForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset= Category.objects.all(),
        required = True
    )
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'categories']

class CategoryForm(forms.ModelForm):
    
    class Meta:
        fields = ('name',)
