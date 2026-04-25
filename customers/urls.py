# customers/urls.py
from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer_list'),
    path('quick-create/', views.CustomerQuickCreateView.as_view(), name='quick_create'),
]