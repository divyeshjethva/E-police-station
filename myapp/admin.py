from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Citizen)
admin.site.register(Complaint)
admin.site.register(MissingPerson)
admin.site.register(Inspector)