from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, ExpenseCategoryForm
from accounting.models import LedgerEntry

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ExpenseCategory.objects.all()
        return context

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')

    def form_valid(self, form):
        with transaction.atomic():
            expense = form.save(commit=False)
            expense.created_by = self.request.user
            expense.save()
            # Create ledger entry
            LedgerEntry.objects.create(
                description=expense.description,
                amount=expense.amount,
                transaction_type='expense',
                reference_id=expense.id,
                user=self.request.user
            )
        messages.success(self.request, 'Expense recorded successfully.')
        return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully.')
        return super().form_valid(form)

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:list')

    def delete(self, request, *args, **kwargs):
        expense = self.get_object()
        # Delete corresponding ledger entry (optional)
        LedgerEntry.objects.filter(transaction_type='expense', reference_id=expense.id).delete()
        messages.success(request, 'Expense deleted.')
        return super().delete(request, *args, **kwargs)

# Optional: Category management
class ExpenseCategoryListView(LoginRequiredMixin, ListView):
    model = ExpenseCategory
    template_name = 'expenses/category_list.html'
    context_object_name = 'categories'

class ExpenseCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = 'expenses/category_form.html'
    success_url = reverse_lazy('expenses:category_list')