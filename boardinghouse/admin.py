from django.contrib import admin
from . models import Landlord, Room, Tenant


admin.site.register(Landlord)
admin.site.register(Room)
admin.site.register(Tenant)
