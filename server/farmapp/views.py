from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .models import AdminActivityLog, User, Product, Order
from .serializers import AdminActivityLogSerializer, UserSerializer, ProductSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q


# View all users
class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = User.objects.all()
        role = request.GET.get('role')
        status = request.GET.get('status')
        
        if role:
            queryset = queryset.filter(role=role)
        if status:
            queryset = queryset.filter(status=status)

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# Detailed View of a specific user
class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(userId=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user_serializer = UserSerializer(user)

        # Fetch activity logs for the user
        activity_logs = AdminActivityLog.objects.filter(admin=user)
        activity_logs_serializer = AdminActivityLogSerializer(activity_logs, many=True)

        response_data = {
            "user": user_serializer.data,
            "activity_logs": activity_logs_serializer.data
        }

        return Response(response_data)

# Activate/Deactivate User
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def UserStatusUpdateView(request, userId):
    user = get_object_or_404(User, user_id=userId)
    new_status = request.data.get('status')

    if new_status not in ['active', 'inactive']:
        return Response({"error": "Invalid status"}, status=400)

    user.status = new_status
    user.save()
    
    # Log the action in Admin Activity Log
    AdminActivityLog.objects.create(
        admin=request.user,
        action=f"Updated user {userId} status to {new_status}"
    )
    
    return Response({"message": "Status updated successfully."})


# Pending Product Approvals
class PendingProductListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Product.objects.filter(status="under_review")
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

# Approve Product
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def approve_product(request, product_id):
    product = get_object_or_404(Product, productId=product_id)
    product.status = 'in_stock'
    product.save()
    return Response({"message": "Product approved successfully."})

# Reject Product
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def reject_product(request, product_id):
    product = get_object_or_404(Product, productId=product_id)
    rejection_reason = request.data.get('rejection_reason', '')
    product.status = 'rejected'
    product.rejection_reason = rejection_reason  # Make sure this field exists in your model
    product.save()
    return Response({"message": "Product rejected."})

# Product Overview with filtering, sorting, and search
class ProductOverviewView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Product.objects.all()

        # Filtering
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        farmer_id = request.GET.get('farmerId')
        search_query = request.GET.get('search')

        filters = Q()
        if category:
            filters &= Q(category=category)
        if min_price and max_price:
            filters &= Q(unitPrice__gte=min_price, unitPrice__lte=max_price)
        if farmer_id:
            filters &= Q(farmer__farmerId=farmer_id)
        if search_query:
            filters &= Q(productName__icontains=search_query) | Q(description__icontains=search_query)

        queryset = queryset.filter(filters)

        # Sorting
        sort_by = request.GET.get('sort_by', 'unitPrice')
        sort_order = request.GET.get('sort_order', 'asc')
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

# Order Management: List all orders
class OrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        status = request.GET.get('status')
        queryset = Order.objects.all()
        
        if status:
            queryset = queryset.filter(status=status)

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

# Order Details
class OrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, order_id):
        order = get_object_or_404(Order, orderId=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
