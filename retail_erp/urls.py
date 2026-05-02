from django.contrib import admin
from django.urls import path, include
from reports.views import DashboardView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('users/', include('users.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    path('customers/', include('customers.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('purchases/', include('purchases.urls')),
    path('accounting/', include('accounting.urls')),
    path('reports/', include('reports.urls')),
    path('expenses/', include('expenses.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]