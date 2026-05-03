from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm
from users.mixins import ManagerRequiredMixin
from django.db.models import Sum, F, FloatField


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

class StockAnalyticsView(TemplateView):
    template_name = 'inventory/stock_analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Total stock value (cost basis)
        total_value = Product.objects.aggregate(total=Sum(F('stock') * F('cost')))['total'] or 0
        context['total_stock_value'] = total_value

        # Low stock products (stock <= reorder_level)
        low_stock = Product.objects.filter(stock__lte=F('reorder_level')).select_related('category')
        context['low_stock_products'] = low_stock

        # Stock by category (count of products and total stock)
        categories = Category.objects.annotate(
            product_count=Sum('products__stock', default=0)
        ).values('name', 'product_count')
        context['categories'] = categories

        # Top 5 most stocked products
        top_stocked = Product.objects.order_by('-stock')[:5]
        context['top_stocked'] = top_stocked
        return context