from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from .models import PurchaseOrder, PurchaseItem
from .forms import PurchaseOrderForm, PurchaseItemForm
from inventory.models import Product

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
            context['item_form'] = PurchaseItemForm(self.request.POST)
        else:
            context['item_form'] = PurchaseItemForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        item_form = PurchaseItemForm(request.POST)
        if form.is_valid() and item_form.is_valid():
            return self.form_valid(form, item_form)
        else:
            return self.form_invalid(form, item_form)

    def form_valid(self, form, item_form):
        with transaction.atomic():
            order = form.save()
            # Create single item (simplified; for multiple items we'd use formsets)
            product = item_form.cleaned_data['product']
            quantity = item_form.cleaned_data['quantity']
            cost = item_form.cleaned_data['cost']
            PurchaseItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                cost=cost
            )
            order.total = quantity * cost
            order.save()
        messages.success(self.request, 'Purchase order created.')
        return redirect(self.success_url)

    def form_invalid(self, form, item_form):
        return self.render_to_response(self.get_context_data(form=form, item_form=item_form))

class ReceivePurchaseView(UpdateView):
    model = PurchaseOrder
    fields = []  # just use post to change status
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