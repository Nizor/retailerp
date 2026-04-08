# reports/views.py
from django.views.generic import TemplateView, ListView
from django.db.models import Sum, Count, F, Q
from sales.models import Transaction, TransactionItem
from inventory.models import Product
from datetime import date, timedelta

class DashboardView(TemplateView):
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        # Daily sales
        daily_sales = Transaction.objects.filter(created_at__date=today).aggregate(
            total=Sum('total'), count=Count('id')
        )
        context['daily_sales_total'] = daily_sales['total'] or 0
        context['daily_sales_count'] = daily_sales['count'] or 0

        # Top products
        top_products = TransactionItem.objects.values('product__name').annotate(
            total_qty=Sum('quantity')
        ).order_by('-total_qty')[:5]
        context['top_products'] = top_products

        # Low stock products
        low_stock = Product.objects.filter(stock__lte=F('reorder_level')).only('name', 'stock', 'reorder_level')[:10]
        context['low_stock'] = low_stock

        return context

class ReportIndexView(TemplateView):
    template_name = 'reports/index.html'

class DailySalesReportView(ListView):
    model = Transaction
    template_name = 'reports/daily_sales.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        today = date.today()
        return Transaction.objects.filter(
            created_at__date=today,
            status='completed'
        ).select_related('user', 'customer').prefetch_related('items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        total = Transaction.objects.filter(created_at__date=today, status='completed').aggregate(total=Sum('total'))['total'] or 0
        context['daily_total'] = total
        context['date'] = today
        return context