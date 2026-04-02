from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import UserProfile

class RegisterView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create profile with default role cashier
        UserProfile.objects.create(user=self.object, role='cashier')
        return response