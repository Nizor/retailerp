from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from users.mixins import ManagerRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    queryset = Product.objects.select_related('category').all()

class ProductCreateView(ManagerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')