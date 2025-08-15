from django.contrib import admin
from .models import Aircraft, MaintenanceLog

admin.site.register(Aircraft)
admin.site.register(MaintenanceLog)
