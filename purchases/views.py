from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from .models import PurchaseOrder, PurchaseItem
from .forms import PurchaseOrderForm, PurchaseItemFormSet

class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = 'purchases/purchase_list.html'
    context_object_name = 'orders'
    ordering = ['-order_date']

class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchases/purchase_form.html'
    success_url = reverse_lazy('purchases:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseItemFormSet(self.request.POST)
        else:
            context['formset'] = PurchaseItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.total = 0
            self.object.save()
            if formset.is_valid():
                total = 0
                for item_form in formset:
                    if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                        item = item_form.save(commit=False)
                        item.order = self.object
                        item.total = item.quantity * item.cost
                        item.save()
                        total += item.total
                self.object.total = total
                self.object.save()
                messages.success(self.request, 'Purchase order created successfully.')
                return redirect(self.success_url)
            else:
                self.object.delete()  # rollback
                return self.form_invalid(form)
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class ReceivePurchaseView(UpdateView):
    model = PurchaseOrder
    fields = []
    template_name = 'purchases/receive_confirm.html'
    success_url = reverse_lazy('purchases:list')

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == 'pending':
            with transaction.atomic():
                for item in order.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
                order.status = 'received'
                order.save()
            messages.success(request, f'Purchase order #{order.id} received. Stock updated.')
        else:
            messages.error(request, 'Order already received or cancelled.')
        return redirect(self.success_url)