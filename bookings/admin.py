from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.utils import timezone
from .models import CustomUser, Booking


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for user management with role and country-based features
    Super Admin can create/delete Admins and Technicians
    """
    list_display = ('username', 'email', 'role', 'country', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('role', 'country', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'country', 'phone_number')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'country', 'phone_number')}),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Super admin sees all users
        if hasattr(request.user, 'role') and request.user.role == 'super_admin':
            return qs
        # Admins see only technicians
        elif hasattr(request.user, 'role') and request.user.role == 'admin':
            return qs.filter(Q(role='technician') | Q(id=request.user.id))
        # Technicians can only see themselves
        elif hasattr(request.user, 'role') and request.user.role == 'technician':
            return qs.filter(id=request.user.id)
        return qs
    
    def has_add_permission(self, request):
        # Only super_admin and admin can add users
        if hasattr(request.user, 'role'):
            return request.user.role in ['super_admin', 'admin']
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Only super_admin can delete admins
        # Admins can delete technicians
        if not hasattr(request.user, 'role'):
            return False
        
        if request.user.role == 'super_admin':
            return True
        elif request.user.role == 'admin' and obj:
            # Admins can only delete technicians
            return obj.role == 'technician'
        return False
    
    def has_change_permission(self, request, obj=None):
        if not hasattr(request.user, 'role'):
            return False
            
        if request.user.role == 'super_admin':
            return True
        elif request.user.role == 'admin':
            # Admins can change themselves and technicians
            if obj:
                return obj.role == 'technician' or obj.id == request.user.id
            return True
        elif request.user.role == 'technician':
            # Technicians can only change themselves
            if obj:
                return obj.id == request.user.id
            return False
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Comprehensive admin for fumigation order management
    """
    list_display = (
        'order_number',
        'order_time',
        'country_badge',
        'location_short',
        'client_phone',
        'pest_type',
        'amount',
        'status_badge',
        'assigned_technician',
        'complaint_indicator',
    )
    
    list_filter = (
        'status',
        'country',
        'pest_type',
        'assigned_technician',
        'has_complaint',
        'order_time',
    )
    
    search_fields = (
        'order_number',
        'client_phone',
        'location_pin',
        'location_address',
        'notes',
    )
    
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'created_by', 'assigned_at', 'completed_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'order_time', 'country', 'status')
        }),
        ('Location Details', {
            'fields': ('location_pin', 'location_address')
        }),
        ('Contact Information', {
            'fields': ('client_phone',)
        }),
        ('Service Details', {
            'fields': ('pest_type', 'amount')
        }),
        ('Assignment', {
            'fields': ('assigned_technician', 'assigned_at'),
            'description': 'Admins can assign orders at any time. Technicians can only view in the morning (5 AM - 12 PM).'
        }),
        ('Complaint Status', {
            'fields': ('has_complaint', 'complaint_details'),
            'description': 'Track if client complained about service'
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'order_time'
    
    actions = ['assign_to_technician', 'mark_as_completed', 'mark_has_complaint', 'mark_no_complaint']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Technicians can only see orders in their country
        if hasattr(request.user, 'role') and request.user.role == 'technician':
            if request.user.country:
                return qs.filter(
                    assigned_technician=request.user,
                    country=request.user.country
                )
            return qs.filter(assigned_technician=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new order
            obj.created_by = request.user
        
        # Track assignment time
        if 'assigned_technician' in form.changed_data and obj.assigned_technician:
            obj.assigned_at = timezone.now()
            if obj.status == 'pending':
                obj.status = 'assigned'
        
        # Track completion time
        if 'status' in form.changed_data and obj.status == 'completed':
            obj.completed_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def country_badge(self, obj):
        """Display country with flag emoji"""
        flags = {
            'kenya': '🇰🇪',
            'uganda': '🇺🇬',
            'zambia': '🇿🇲',
            'south_africa': '🇿🇦',
        }
        flag = flags.get(obj.country, '🌍')
        return format_html(
            '<span style="font-size: 16px;">{} {}</span>',
            flag,
            obj.get_country_display()
        )
    country_badge.short_description = 'Country'
    
    def location_short(self, obj):
        """Show shortened location"""
        if len(obj.location_pin) > 30:
            return obj.location_pin[:30] + '...'
        return obj.location_pin
    location_short.short_description = 'Location'
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#ffc107',
            'assigned': '#17a2b8',
            'in_progress': '#007bff',
            'completed': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def complaint_indicator(self, obj):
        """Visual indicator of complaints"""
        if obj.has_complaint:
            return format_html(
                '<span style="color: #dc3545; font-size: 18px; font-weight: bold;" title="Client Complained">⚠️ YES</span>'
            )
        else:
            return format_html(
                '<span style="color: #28a745; font-size: 18px; font-weight: bold;" title="No Complaint">✅ NO</span>'
            )
    complaint_indicator.short_description = 'Complained?'
    
    @admin.action(description='Assign to Technician')
    def assign_to_technician(self, request, queryset):
        self.message_user(request, 'Select technician in the order detail page.')
    
    @admin.action(description='Mark as Completed')
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} orders marked as completed.')
    
    @admin.action(description='Mark as "Has Complaint"')
    def mark_has_complaint(self, request, queryset):
        updated = queryset.update(has_complaint=True)
        self.message_user(request, f'{updated} orders marked with complaint.')
    
    @admin.action(description='Mark as "No Complaint"')
    def mark_no_complaint(self, request, queryset):
        updated = queryset.update(has_complaint=False, complaint_details='')
        self.message_user(request, f'{updated} orders marked with no complaint.')
    
    def changelist_view(self, request, extra_context=None):
        """Add dashboard statistics to the order list view"""
        extra_context = extra_context or {}
        
        # Get queryset based on user role
        qs = self.get_queryset(request)
        
        # Calculate statistics
        total_orders = qs.count()
        pending_orders = qs.filter(status='pending').count()
        assigned_orders = qs.filter(status='assigned').count()
        completed_orders = qs.filter(status='completed').count()
        
        # Complaint tracking
        completed_qs = qs.filter(status='completed')
        orders_with_complaints = completed_qs.filter(has_complaint=True).count()
        orders_no_complaints = completed_qs.filter(has_complaint=False).count()
        
        # Today's orders
        today = timezone.now().date()
        today_orders = qs.filter(order_time__date=today).count()
        
        # Group by country
        country_stats = qs.values('country').annotate(count=Count('id'))
        
        extra_context['dashboard_stats'] = {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'assigned_orders': assigned_orders,
            'completed_orders': completed_orders,
            'orders_with_complaints': orders_with_complaints,
            'orders_no_complaints': orders_no_complaints,
            'today_orders': today_orders,
            'country_stats': country_stats,
        }
        
        return super().changelist_view(request, extra_context=extra_context)


# Customize admin site headers
admin.site.site_header = "Sanok Fumigation - Order Management System"
admin.site.site_title = "Sanok Fumigation Admin"
admin.site.index_title = "Welcome to Fumigation Order Management Dashboard"
