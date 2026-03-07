from django.urls import path
from . import views

urlpatterns = [
    # Authentication — shared entry point
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
