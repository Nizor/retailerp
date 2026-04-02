from django.views.generic import TemplateView

class LedgerView(TemplateView):
    template_name = 'accounting/ledger.html'