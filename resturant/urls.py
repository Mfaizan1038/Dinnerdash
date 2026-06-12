from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='item_list'),
    path('items/<int:pk>', views.item_detail, name='item_detail'),
    path('cart/', views.cart_view, name= 'cart_view'),
    path('cart/add/<int:item_id>/',views.cart_add, name='cart_add'),
    path('cart/update<int:item_id>/',views.cart_update, name='cart_update'),
    path('cart/remove<int:item_id>/',views.cart_remove, name='cart_remove'),
    path('checkout/',views.checkout, name='checkout'),
    path('orders/',views.order_history, name='order_history'),
    path('orders/<int:pk>/', views.order_detail,name='order_detail'),
    path('admin-panel/items/new/',views.admin_item_create, name='admin_item_create'),
    path('admin-panel/items/<int:pk>/edit/', views.admin_item_edit, name='admin_item_edit'),
    path('admin-panel/items/<int:pk>/retire/', views.admin_item_retire, name='admin_item_retire'),
    path('admin-panel/categories/',views.admin_category_list, name='admin_category_list'),
    path('admin-panel/categories/new/', views.admin_category_create, name='admin_category_create'),
    path('admin-panel/categories/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('admin-panel/',views.admin_dashboard, name= 'admin_dashboard'),
    path('admin-panel/orders/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-panel/orders/<int:pk>/<str:action>/', views.admin_order_transition, name='admin_order_transition'),

]