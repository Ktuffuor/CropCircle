from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .models import User, Product, Order
from .serializers import AdminActivityLogSerializer, UserSerializer, ProductSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q


class UserPagination(PageNumberPagination):
    page_size = 20

class UserListView(APIView):
    def get(self, request):
        # Get query parameters
        role = request.query_params.get('role')
        status = request.query_params.get('status')
        
        # Query users
        users = User.objects.all()
        if role:
            users = users.filter(role=role)
        if status:
            users = users.filter(status=status)
        
        # Apply pagination
        paginator = UserPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        
        return paginator.get_paginated_response(serializer.data)


# Detailed View of a specific user
class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(userId=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Activate/Deactivate User
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

@permission_classes([IsAuthenticated, IsAdminUser])
class UserStatusUpdateView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(userId=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status = request.data.get('status')
        if status not in ['active', 'inactive']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.status = status
        user.save()
        return Response({'message': 'User status updated successfully'})



# Pending Product Approvals
@permission_classes([IsAuthenticated, IsAdminUser])
class PendingProductApprovalsView(APIView):
    def get(self, request):
        # Query products with status "under_review"
        products = Product.objects.filter(status='under_review')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Approve Product
@permission_classes([IsAuthenticated, IsAdminUser])
class ApproveProductView(APIView):
    def put(self, request, product_id):
        try:
            product = Product.objects.get(productId=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.status = 'in_stock'
        product.save()
        return Response({'message': 'Product approved successfully'})

# Reject Product
@permission_classes([IsAuthenticated, IsAdminUser])
class RejectProductView(APIView):
    def put(self, request, product_id):
        try:
            product = Product.objects.get(productId=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        rejection_reason = request.data.get('rejectionReason', 'No reason provided')
        product.status = 'out_of_stock'
        product.rejectionReason = rejection_reason
        product.save()
        return Response({'message': 'Product rejected successfully', 'rejectionReason': rejection_reason})


# Product Overview with filtering, sorting, and search
class ProductOverviewView(APIView):
    def get(self, request):
        # Get query parameters
        category = request.query_params.get('category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        farmer_id = request.query_params.get('farmer_id')
        search = request.query_params.get('search')
        sort_by = request.query_params.get('sort_by', 'productName')  # Default sorting by product name
        
        # Query products
        products = Product.objects.all()

        # Apply filters
        if category:
            products = products.filter(category=category)
        if min_price:
            products = products.filter(unitPrice__gte=min_price)
        if max_price:
            products = products.filter(unitPrice__lte=max_price)
        if farmer_id:
            products = products.filter(farmer_id=farmer_id)
        
        # Apply search using a lambda function
        if search:
            products = filter(lambda product: search.lower() in product.productName.lower(), products)
        
        # Apply sorting using a lambda function
        products = sorted(products, key=lambda product: getattr(product, sort_by))

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Order Management: List all orders
class OrderPagination(PageNumberPagination):
    page_size = 20

@permission_classes([IsAuthenticated, IsAdminUser])
class OrderListView(APIView):
    def get(self, request):
        # Get query parameters
        status = request.query_params.get('status')
        payment_method = request.query_params.get('payment_method')
        date_range = request.query_params.get('date_range')
        
        # Query orders
        orders = Order.objects.all()
        if status:
            orders = orders.filter(status=status)
        if payment_method:
            orders = orders.filter(payment_method=payment_method)
        if date_range:
            start_date, end_date = date_range.split(',')
            orders = orders.filter(createdAt__range=[start_date, end_date])
        
        # Apply pagination
        paginator = OrderPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        
        return paginator.get_paginated_response(serializer.data)

@permission_classes([IsAuthenticated, IsAdminUser])
class OrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(orderId=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)


@permission_classes([IsAuthenticated, IsAdminUser])
class OrderStatusUpdateView(APIView):
    def put(self, request, order_id):
        try:
            order = Order.objects.get(orderId=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
        new_status = request.data.get('status')
        if new_status not in [choice[0] for choice in Order.ORDER_STATUS_CHOICES]:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        return Response({'message': 'Order status updated successfully'})
