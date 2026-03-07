from django.urls import path
from . import views

app_name = 'super_admin'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
    path('users/<int:pk>/toggle/', views.user_toggle_active_view, name='user_toggle'),
    path('orders/', views.order_list_view, name='order_list'),
]
