from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm
from sales.models import Transaction

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)
            )
        return queryset

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show last 10 transactions
        context['transactions'] = Transaction.objects.filter(customer=self.object).select_related('user').order_by('-created_at')[:10]
        return context

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Customer "{self.object.name}" added successfully.')
        return response

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Customer "{self.object.name}" updated successfully.')
        return response

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:list')

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        messages.success(request, f'Customer "{customer.name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)

class CustomerQuickCreateView(View):
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if not name:
            return JsonResponse({'errors': {'name': 'Name is required'}}, status=400)
        customer = Customer.objects.create(name=name, phone=phone, email=email)
        return JsonResponse({'id': customer.id, 'name': customer.name})