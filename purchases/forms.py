from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseItem
from inventory.models import Product

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'expected_date']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'expected_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'cost']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
        }

# Create formset for PurchaseItem (can add extra empty forms)
PurchaseItemFormSet = inlineformset_factory(
    PurchaseOrder, 
    PurchaseItem, 
    form=PurchaseItemForm,
    extra=3,          # show 3 empty item rows
    can_delete=True
)