from django.shortcuts import redirect
from django.urls import reverse_lazy


def check_permission(request, permission):
    if request.user.is_admin:
        return True
    if permission in list(request.user.group_id.permissions.values_list('codename', flat=True)):
        return True
    return False


class CheckPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if check_permission(self.request, self.permission_name) is False:
            return redirect(reverse_lazy('core:unauthorized'))
        else:
            return super(CheckPermissionMixin, self).dispatch(self.request, *args, **kwargs)


class SuperAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            return redirect(reverse_lazy('core:unauthorized'))
        else:
           return super(SuperAdminMixinx, self).dispatch(self.request, *args, **kwargs) 