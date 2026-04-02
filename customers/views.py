# customers/views.py
from django.views.generic import TemplateView

class CustomerListView(TemplateView):
    template_name = 'customers/customer_list.html'