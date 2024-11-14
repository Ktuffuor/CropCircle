from django.urls import path

from . import views

urlpatterns = [
    path('api/admin/users/', views.UserListView.as_view(), name='user-list'),
    path('api/admin/users/<int:userId>', views.UserDetailView.as_view(), name='user-detail'),
    path('api/admin/user/<int:userId>/status/', views.UserStatusUpdateView.as_view(), name='user-status-update'),
    path('api/admin/products/pending/', views.PendingProductListView.as_view(), name='pending-products'),
    path('api/admin/products/<int:productId>/approve/', views.approve_product, name='approve-product'),
    path('api/admin/products/<int:productId>/reject/', views.reject_product, name='reject-product'),
    path('api/admin/products/', views.ProductOverviewView.as_view(), name='product-overview'),
    path('api/admin/orders/', views.OrderListView.as_view(), name='order-list'),
    path('api/admin/orders/<int:orderId>', views.OrderDetailView.as_view(), name='order-detail'),
]