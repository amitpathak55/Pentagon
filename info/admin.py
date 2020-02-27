from django.contrib import admin
from .models import Student, Undergrad, Masters, Phd, Employment


admin.site.register(Student)
admin.site.register(Undergrad)
admin.site.register(Masters)
admin.site.register(Phd)
admin.site.register(Employment)



