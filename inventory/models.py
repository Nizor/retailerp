from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        unique_together = [['name', 'category']]   # group name unique per category

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)  # auto‑generated
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Markup % applied to cost to get price")
    auto_price_from_markup = models.BooleanField(default=True, help_text="If checked, price = cost * (1 + markup/100)")
    stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['group']),
        ]

    def save(self, *args, **kwargs):
        # Auto‑generate barcode if not provided
        if not self.barcode:
            self.barcode = self.generate_barcode()
        # Auto‑calculate price from cost + markup if enabled
        if self.auto_price_from_markup:
            self.price = self.cost * (1 + (self.markup_percentage / 100))
        super().save(*args, **kwargs)

    def generate_barcode(self):
        # Simple unique barcode: "PRD" + zero‑padded ID (will be assigned after first save)
        # We'll handle it by using a temporary value and then update after save if needed.
        # Alternative: use uuid or timestamp.
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:13].upper()

    def __str__(self):
        return self.name
    