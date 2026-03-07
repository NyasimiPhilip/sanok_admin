from django.urls import path
from . import views

app_name = 'technician'

urlpatterns = [
    path('', views.orders_view, name='orders'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:pk>/status/', views.update_status_view, name='update_status'),
]
