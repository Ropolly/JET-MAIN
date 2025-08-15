from django.contrib import admin
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine
)

# Register models
admin.site.register(Modification)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(FBO)
admin.site.register(Ground)
admin.site.register(Airport)
admin.site.register(Document)
admin.site.register(Aircraft)
admin.site.register(Transaction)
admin.site.register(Agreement)
admin.site.register(Patient)
admin.site.register(Quote)
admin.site.register(Passenger)
admin.site.register(CrewLine)
admin.site.register(Trip)
admin.site.register(TripLine)
