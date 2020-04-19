from django.conf import settings
from django.utils.translation import activate
import re
from django.utils.deprecation import MiddlewareMixin


class ForceDefaultLanguage(MiddlewareMixin):
    def process_request(self, request):
        if re.match('.*cms/', request.path):
            activate(settings.LANGUAGE_CODE)
