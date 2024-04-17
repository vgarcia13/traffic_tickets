from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Vehicle)
admin.site.register(Officer)
admin.site.register(Ticket)
