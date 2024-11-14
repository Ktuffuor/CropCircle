from django.contrib import admin
from .models import User, Farmer, Order, Product, AdminActivityLog

admin.site.register(User)
admin.site.register(Farmer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(AdminActivityLog)