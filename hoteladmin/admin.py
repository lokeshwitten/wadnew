from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Dish)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(address)
admin.site.register(Global)
admin.site.register(Reservations)
admin.site.register(Item)

