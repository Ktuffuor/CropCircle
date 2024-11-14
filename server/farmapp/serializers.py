from rest_framework import serializers
from .models import AdminActivityLog, User, Farmer, Product, Order

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'name', 'email', 'role', 'phone', 'address', 'createdAt', 'updatedAt']

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'productName', 'description', 'category', 'unitPrice', 'stockQuantity', 'status', 'createdAt', 'updatedAt']

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer()  # Nest UserSerializer to include customer details

    class Meta:
        model = Order
        fields = ['orderId', 'customer', 'orderItems', 'totalAmount', 'status', 'createdAt', 'updatedAt']


class AdminActivityLogSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)

    class Meta:
        model = AdminActivityLog
        fields = ['logId', 'admin', 'action', 'targetId', 'timestamp']