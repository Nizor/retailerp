# suppliers/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Supplier
from .forms import SupplierForm

class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(contact_person__icontains=search) | 
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Supplier "{self.object.name}" added successfully.')
        return response

class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Supplier "{self.object.name}" updated successfully.')
        return response

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers:list')

    def delete(self, request, *args, **kwargs):
        supplier = self.get_object()
        messages.success(request, f'Supplier "{supplier.name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)