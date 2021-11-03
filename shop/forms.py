from django import forms
from .models import ProductFilter, ProductComment

class PriceFilterForm(forms.ModelForm):
    class Meta:
        model = ProductFilter
        fields = ('price1','price2')

class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('author', 'email', 'website', 'text')
