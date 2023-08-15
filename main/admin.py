from django.contrib import admin
from .models import User, Employee, Employer, Jobapplication, Response

# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Jobapplication)
admin.site.register(Response)

