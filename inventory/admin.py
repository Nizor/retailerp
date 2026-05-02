from django.contrib import admin
from .models import Category, Group, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'group', 'cost', 'price', 'stock', 'is_active')
    list_filter = ('category', 'group', 'is_active')
    search_fields = ('name', 'sku', 'barcode')