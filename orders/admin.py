from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Topping)
admin.site.register(LineItem)
admin.site.register(Order)