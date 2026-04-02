from django.views.generic import TemplateView

class SupplierListView(TemplateView):
    template_name = 'suppliers/supplier_list.html'