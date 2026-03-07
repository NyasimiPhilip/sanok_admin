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
        # Time restriction disabled - technicians can access anytime
        # Order visibility is controlled in views
        response = self.get_response(request)
        return response
        return response
