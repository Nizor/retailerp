from django import forms
from .models import PurchaseOrder, PurchaseItem
from inventory.models import Product

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_date']

class PurchaseItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True))
    quantity = forms.IntegerField(min_value=1)
    cost = forms.DecimalField(max_digits=10, decimal_places=2)