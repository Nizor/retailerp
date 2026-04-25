# purchases/urls.py
from django.urls import path
from . import views

app_name = 'purchases'
urlpatterns = [
    path('',views.PurchaseOrderListView.as_view(), name='list'),
    path('create/', views.PurchaseOrderCreateView.as_view(), name='create'),
    path('<int:pk>/receive/', views.ReceivePurchaseView.as_view(), name='receive'),
]