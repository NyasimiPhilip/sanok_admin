from django.utils import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import render


class TechnicianAccessTimeMiddleware:
    """
    Middleware to restrict technician access to morning hours (5 AM - 12 PM)
    DISABLED: Technicians can now access anytime but only see current day's orders
    Order visibility is controlled in views (technicians see only current day's orders)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if getattr(request, 'user', None) and request.user.is_authenticated:
            role = getattr(request.user, 'role', None)
            should_be_staff = role in ('admin', 'super_admin')
            should_be_superuser = role == 'super_admin'
            updates = []

            if request.user.is_staff != should_be_staff:
                request.user.is_staff = should_be_staff
                updates.append('is_staff')

            if request.user.is_superuser != should_be_superuser:
                request.user.is_superuser = should_be_superuser
                updates.append('is_superuser')

            if updates:
                request.user.save(update_fields=updates)

        # Time restriction disabled - technicians can access anytime
        # Order visibility is controlled in views
        response = self.get_response(request)
        return response
        return response
