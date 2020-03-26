import re
from django.utils.deprecation import MiddlewareMixin


class PermissionListGenerator(MiddlewareMixin):
    def process_request(self, request):
        if re.match('.*cms/', request.path):
            if not request.user.is_anonymous:
                group = request.user.group_id
                if group is None:
                    request.permissions = True
                else:
                    request.permissions = group.permissions.all().values_list('codename', flat=True)
