from django.views.generic import TemplateView

class PurchaseListView(TemplateView):
    template_name = 'purchases/purchase_list.html'