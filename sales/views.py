from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, TransactionItem
from inventory.models import Product

class POSView(LoginRequiredMixin, View):
    template_name = 'sales/pos.html'

    def get(self, request):
        # Retrieve cart from session
        cart = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart.keys()).only('id', 'name', 'price')
        cart_items = []
        total = 0
        for product in products:
            qty = cart[str(product.id)]
            item_total = product.price * qty
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total': item_total,
            })
        context = {
            'cart_items': cart_items,
            'total': total,
            'products': Product.objects.filter(is_active=True).only('id', 'name', 'price', 'stock')[:50],  # limit for performance
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Handle add to cart, remove, checkout, etc.
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if action == 'add':
            cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        elif action == 'remove':
            cart.pop(str(product_id), None)
        elif action == 'checkout':
            # Create transaction and clear cart
            # ... (implement checkout logic)
            pass

        request.session['cart'] = cart
        return redirect('sales:pos')