# sales/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .services import POSService
from inventory.models import Product
from django.views.generic import DetailView
from .models import Transaction

class POSView(LoginRequiredMixin, View):
    template_name = 'sales/pos.html'
    login_url = '/users/login/'   # absolute URL to avoid namespace issues

    def get(self, request):
        cart = request.session.get('cart', {})
        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids).only('id', 'name', 'price')
        cart_items = []
        total = 0
        for product in products:
            qty = cart[str(product.id)]
            item_total = product.price * qty
            total += float(item_total)
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total': item_total,
            })
        context = {
            'cart_items': cart_items,
            'total': total,
            'products': Product.objects.filter(is_active=True).only('id', 'name', 'price', 'stock')[:50],
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if action == 'add':
            product = get_object_or_404(Product, id=product_id)
            if product.stock < quantity:
                messages.error(request, f"Not enough stock for {product.name}")
                return redirect('sales:pos')
            cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
            request.session['cart'] = cart

        elif action == 'remove':
            cart.pop(str(product_id), None)
            request.session['cart'] = cart

        elif action == 'checkout':
            try:
                sale = POSService.process_checkout(cart, request.user)
                # Clear cart after successful checkout
                request.session['cart'] = {}
                messages.success(request, f"Sale completed! Transaction #{sale.id}")
                return redirect('sales:receipt', pk=sale.id)
            except ValueError as e:
                messages.error(request, str(e))

        return redirect('sales:pos')
    
    
class ReceiptView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'sales/receipt.html'
    context_object_name = 'transaction'
    login_url = '/users/login/'   # absolute URL to avoid namespace issues  