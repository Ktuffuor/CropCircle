from django.urls import path
from .views import ApproveProductView, OrderDetailView, OrderListView, OrderStatusUpdateView, PendingProductApprovalsView, ProductOverviewView, RejectProductView, UserDetailView, UserListView

urlpatterns = [

    path('admin/users/', UserListView.as_view(), name='user-list'),

    path('admin/users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),

    path('admin/products/pending/', PendingProductApprovalsView.as_view(), name='pending-product-approvals'),

    path('admin/products/pending/', PendingProductApprovalsView.as_view(), name='pending-product-approvals'),

    path('admin/products/<int:product_id>/approve/', ApproveProductView.as_view(), name='approve-product'),

    path('admin/products/<int:product_id>/reject/', RejectProductView.as_view(), name='reject-product'),

    path('admin/products/', ProductOverviewView.as_view(), name='product-overview'),

    path('admin/orders/', OrderListView.as_view(), name='order-list'),

    path('admin/orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),

    path('admin/orders/<int:order_id>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]
