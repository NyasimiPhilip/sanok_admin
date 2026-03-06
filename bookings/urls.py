from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Bookings/Orders
    path('bookings/', views.booking_list_view, name='booking_list'),
    path('bookings/create/', views.booking_create_view, name='booking_create'),
    path('bookings/<int:pk>/', views.booking_detail_view, name='booking_detail'),
    path('bookings/<int:pk>/edit/', views.booking_edit_view, name='booking_edit'),
    path('bookings/<int:pk>/delete/', views.booking_delete_view, name='booking_delete'),
    path('bookings/<int:pk>/status/', views.booking_status_update_view, name='booking_status_update'),
    path('bookings/<int:pk>/complaint/', views.booking_complaint_toggle_view, name='booking_complaint_toggle'),
    
    # User Management
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:pk>/', views.user_detail_view, name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
    path('users/<int:pk>/toggle-active/', views.user_toggle_active_view, name='user_toggle_active'),
]
