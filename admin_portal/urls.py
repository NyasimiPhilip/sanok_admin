from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/create/', views.order_create_view, name='order_create'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_edit_view, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete_view, name='order_delete'),
    path('orders/<int:pk>/assign/', views.assign_technician_view, name='assign_technician'),
    path('technicians/', views.technician_list_view, name='technician_list'),
]
