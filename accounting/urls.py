# accounting/urls.py
from django.urls import path
from . import views

app_name = 'accounting'
urlpatterns = [
    path('', views.LedgerView.as_view(), name='ledger'),
]