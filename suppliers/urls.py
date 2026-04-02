# suppliers/urls.py
from django.urls import path
from . import views

app_name = 'suppliers'
urlpatterns = [
    path('', views.SupplierListView.as_view(), name='supplier_list'),
]