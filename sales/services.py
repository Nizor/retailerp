# sales/services.py
from decimal import Decimal
from django.db import transaction
from sales.models import Transaction, TransactionItem
from inventory.models import Product
from accounting.models import LedgerEntry
from customers.models import Customer
from django.contrib.auth.models import User

class POSService:
    @staticmethod
    @transaction.atomic
    def process_checkout(cart_data, user: User, customer_id=None, payment_method='cash'):
        """
        cart_data: dict {product_id: quantity}
        """
        if not cart_data:
            raise ValueError("Cart is empty")

        total = Decimal('0.00')
        items_to_create = []
        products_to_update = []

        # Fetch products with select_for_update to avoid race conditions
        product_ids = [int(pid) for pid in cart_data.keys()]
        products = Product.objects.select_for_update().filter(id__in=product_ids)

        for product in products:
            qty = cart_data[str(product.id)]
            if product.stock < qty:
                raise ValueError(f"Insufficient stock for {product.name}")
            item_total = product.price * qty
            total += item_total
            items_to_create.append({
                'product': product,
                'quantity': qty,
                'price': product.price,
                'total': item_total,
            })
            # Reduce stock
            product.stock -= qty
            products_to_update.append(product)

        # Create transaction
        customer = None
        if customer_id:
            customer = Customer.objects.filter(id=customer_id).first()

        sale = Transaction.objects.create(
            user=user,
            customer=customer,
            total=total,
            tax=Decimal('0.00'),  # extend if needed
            discount=Decimal('0.00'),
            payment_method=payment_method,
            status='completed'
        )

        # Create transaction items
        for item in items_to_create:
            TransactionItem.objects.create(
                transaction=sale,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                total=item['total']
            )

        # Update product stocks
        Product.objects.bulk_update(products_to_update, ['stock'])

        # Create ledger entry
        LedgerEntry.objects.create(
            description=f"Sale #{sale.id}",
            amount=total,
            transaction_type='sale',
            reference_id=sale.id,
            user=user
        )

        return sale