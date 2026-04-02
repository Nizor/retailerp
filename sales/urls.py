# sales/urls.py
from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('pos/', views.POSView.as_view(), name='pos'),
]