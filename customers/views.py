# customers/views.py
from django.views.generic import TemplateView, CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Customer

class CustomerListView(TemplateView):
    template_name = 'customers/customer_list.html'

class CustomerQuickCreateView(CreateView):
    model = Customer
    fields = ['name', 'phone', 'email']
    template_name = 'customers/_customer_form.html'

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'id': self.object.id, 'name': self.object.name})
    
    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)