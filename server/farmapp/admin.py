from django.contrib import admin
from .models import User, Order, Product

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userId', 'name', 'email', 'role', 'createdAt', 'updatedAt')
    search_fields = ('name', 'email', 'role')
    list_filter = ('role', 'createdAt')
    ordering = ('-createdAt',)

# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productId', 'productName', 'category', 'unitPrice', 'status', 'createdAt', 'updatedAt')
    search_fields = ('productName', 'category', 'status')
    list_filter = ('category', 'status', 'createdAt')
    ordering = ('-createdAt',)

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'customer', 'totalAmount', 'status', 'createdAt', 'updatedAt')
    search_fields = ('customer__name', 'status')
    list_filter = ('status', 'createdAt')
    ordering = ('-createdAt',)
