# inventory/forms.py
from django import forms
from .models import Product, Group


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'barcode', 'category', 'group', 'cost', 'markup_percentage', 'auto_price_from_markup', 'price', 'stock', 'reorder_level', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'markup_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit group choices to those belonging to selected category (requires JS or initial)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['group'].queryset = Group.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['group'].queryset = self.instance.category.groups.all()