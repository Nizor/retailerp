from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []  # list of role strings: 'admin', 'manager', 'cashier'

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        # UserProfile may not exist for superusers, handle gracefully
        try:
            role = self.request.user.profile.role
        except:
            # Superusers or users without profile are considered admin
            role = 'admin' if self.request.user.is_superuser else None
        if role in self.allowed_roles:
            return True
        raise PermissionDenied("You don't have permission to access this page.")

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin']

class ManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin', 'manager']

class CashierRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin', 'manager', 'cashier']