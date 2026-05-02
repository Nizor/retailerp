# customers/urls.py
from django.urls import path
from . import views

app_name = 'customers'
urlpatterns = [
    path('', views.CustomerListView.as_view(), name='list'),
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='detail'),
    path('create/', views.CustomerCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='delete'),
    path('quick-create/', views.CustomerQuickCreateView.as_view(), name='quick_create'),
]