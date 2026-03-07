from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Booking, BookingCommand, CustomUser
from datetime import datetime


# ============ Authentication Views ============

def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


@login_required
def logout_view(request):
    """Logout"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


@login_required
def home_view(request):
    """Home/landing page"""
    return render(request, 'home.html')


# ============ Dashboard View ============

@login_required
def dashboard_view(request):
    """Dashboard with statistics"""
    user = request.user
    from datetime import datetime, time, timedelta
    
    # Get bookings based on user role and time restrictions
    if hasattr(user, 'role') and user.role == 'technician':
        # Technicians see only their assigned orders from 5 AM of current day
        today = timezone.now().date()
        start_of_day = timezone.make_aware(datetime.combine(today, time(5, 0)))  # 5:00 AM today
        end_of_day = timezone.make_aware(datetime.combine(today, time(23, 59, 59)))
        bookings = Booking.objects.filter(
            assigned_technician=user,
            order_time__gte=start_of_day,
            order_time__lte=end_of_day
        )
    else:
        # Admins and super admins see all orders (up to 2 years ahead)
        two_years_ahead = timezone.now() + timedelta(days=730)
        bookings = Booking.objects.filter(order_time__lte=two_years_ahead)
    
    # Calculate statistics
    completed_bookings = bookings.filter(status='completed')
    stats = {
        'total_orders': bookings.count(),
        'pending_orders': bookings.filter(status='pending').count(),
        'assigned_orders': bookings.filter(status='assigned').count(),
        'in_progress_orders': bookings.filter(status='in_progress').count(),
        'completed_orders': completed_bookings.count(),
        'orders_with_complaints': completed_bookings.filter(has_complaint=True).count(),
        'orders_no_complaints': completed_bookings.filter(has_complaint=False).count(),
        'total_revenue': completed_bookings.aggregate(Sum('amount'))['amount__sum'] or 0,
        'country_stats': bookings.values('country').annotate(count=Count('id')).order_by('-count'),
    }
    
    # Recent orders (filtered by time restrictions)
    recent_orders = bookings.order_by('-order_time')[:10]
    
    # Today's orders for technicians
    today_orders = None
    if user.role == 'technician':
        today_orders = bookings.order_by('order_time')
    
    context = {
        'stats': stats,
        'recent_orders': recent_orders,
        'today_orders': today_orders,
    }
    
    return render(request, 'dashboard.html', context)


# ============ Booking/Order Views ============

@login_required
def booking_list_view(request):
    """List all bookings with filtering"""
    user = request.user
    from datetime import datetime, time, timedelta
    
    # Get bookings based on user role and time restrictions
    if hasattr(user, 'role') and user.role == 'technician':
        # Technicians see only their assigned orders for current day (midnight to midnight)
        today = timezone.now().date()
        start_of_day = timezone.make_aware(datetime.combine(today, time(0, 0)))  # Midnight today
        end_of_day = timezone.make_aware(datetime.combine(today, time(23, 59, 59)))
        bookings = Booking.objects.filter(
            assigned_technician=user,
            order_time__gte=start_of_day,
            order_time__lte=end_of_day
        )
    else:
        # Admins and super admins see all orders (up to 2 years ahead)
        two_years_ahead = timezone.now() + timedelta(days=730)
        bookings = Booking.objects.filter(order_time__lte=two_years_ahead)
    
    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    country_filter = request.GET.get('country')
    if country_filter:
        bookings = bookings.filter(country=country_filter)
    
    pest_type_filter = request.GET.get('pest_type')
    if pest_type_filter:
        bookings = bookings.filter(pest_type=pest_type_filter)
    
    complaint_filter = request.GET.get('has_complaint')
    if complaint_filter == 'yes':
        bookings = bookings.filter(has_complaint=True)
    elif complaint_filter == 'no':
        bookings = bookings.filter(has_complaint=False)
    
    search_query = request.GET.get('search')
    if search_query:
        bookings = bookings.filter(
            Q(order_number__icontains=search_query) |
            Q(client_phone__icontains=search_query) |
            Q(location_address__icontains=search_query)
        )
    
    bookings = bookings.order_by('-order_time')
    
    # Pagination
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookings': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'booking_list.html', context)


@login_required
def booking_detail_view(request, pk):
    """Detail view for a single booking"""
    user = request.user
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    if hasattr(user, 'role') and user.role == 'technician':
        if booking.assigned_technician != user:
            messages.error(request, 'You do not have permission to view this booking')
            return redirect('booking_list')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'booking_detail.html', context)


@login_required
def booking_create_view(request):
    """Create a new booking"""
    user = request.user
    
    # Only admins and super admins can create bookings
    if not (user.is_super_admin() or user.is_admin()):
        messages.error(request, 'You do not have permission to create bookings')
        return redirect('booking_list')
    
    if request.method == 'POST':
        try:
            booking = Booking.objects.create(
                order_time=datetime.fromisoformat(request.POST.get('order_time')),
                country=request.POST.get('country'),
                location_pin=request.POST.get('location_pin'),
                location_address=request.POST.get('location_address'),
                client_phone=request.POST.get('client_phone'),
                pest_type=request.POST.get('pest_type'),
                amount=float(request.POST.get('amount')),
                status=request.POST.get('status', 'pending'),
                notes=request.POST.get('notes', ''),
                created_by=user,
            )
            
            # Assign technician if selected
            technician_id = request.POST.get('assigned_technician')
            if technician_id:
                technician = CustomUser.objects.get(pk=technician_id)
                booking.assigned_technician = technician
                booking.assigned_at = timezone.now()
                if booking.status == 'pending':
                    booking.status = 'assigned'
                booking.save()
            
            messages.success(request, f'Order {booking.order_number} created successfully!')
            return redirect('booking_detail', pk=booking.pk)
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    # Get technicians for assignment
    technicians = CustomUser.objects.filter(role='technician', is_active=True)
    
    context = {
        'technicians': technicians,
    }
    
    return render(request, 'booking_form.html', context)


@login_required
def booking_edit_view(request, pk):
    """Edit an existing booking"""
    user = request.user
    booking = get_object_or_404(Booking, pk=pk)
    
    # Only admins and super admins can edit bookings
    if not (user.is_super_admin() or user.is_admin()):
        messages.error(request, 'You do not have permission to edit bookings')
        return redirect('booking_detail', pk=pk)
    
    if request.method == 'POST':
        try:
            booking.order_time = datetime.fromisoformat(request.POST.get('order_time'))
            booking.country = request.POST.get('country')
            booking.location_pin = request.POST.get('location_pin')
            booking.location_address = request.POST.get('location_address')
            booking.client_phone = request.POST.get('client_phone')
            booking.pest_type = request.POST.get('pest_type')
            booking.amount = float(request.POST.get('amount'))
            booking.status = request.POST.get('status')
            booking.notes = request.POST.get('notes', '')
            booking.has_complaint = request.POST.get('has_complaint') == 'on'
            booking.complaint_details = request.POST.get('complaint_details', '')
            
            # Assign technician if changed
            technician_id = request.POST.get('assigned_technician')
            if technician_id:
                technician = CustomUser.objects.get(pk=technician_id)
                if booking.assigned_technician != technician:
                    booking.assigned_technician = technician
                    booking.assigned_at = timezone.now()
            else:
                booking.assigned_technician = None
                booking.assigned_at = None
            
            booking.save()
            messages.success(request, f'Order {booking.order_number} updated successfully!')
            return redirect('booking_detail', pk=booking.pk)
        except Exception as e:
            messages.error(request, f'Error updating booking: {str(e)}')
    
    # Get technicians for assignment
    technicians = CustomUser.objects.filter(role='technician', is_active=True)
    
    context = {
        'booking': booking,
        'technicians': technicians,
    }
    
    return render(request, 'booking_form.html', context)


@login_required
def booking_delete_view(request, pk):
    """Delete a booking"""
    user = request.user
    booking = get_object_or_404(Booking, pk=pk)
    
    # Only admins and super admins can delete bookings
    if not (user.is_super_admin() or user.is_admin()):
        messages.error(request, 'You do not have permission to delete bookings')
        return redirect('booking_detail', pk=pk)
    
    if request.method == 'POST':
        order_number = booking.order_number
        booking.delete()
        messages.success(request, f'Order {order_number} deleted successfully!')
        return redirect('booking_list')
    
    return redirect('booking_detail', pk=pk)


@login_required
def booking_status_update_view(request, pk):
    """Update booking status"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        booking.status = new_status
        
        if new_status == 'completed':
            booking.completed_at = timezone.now()
        
        booking.save()
        messages.success(request, f'Order status updated to {booking.get_status_display()}')
    
    return redirect('booking_detail', pk=pk)


@login_required
def booking_complaint_toggle_view(request, pk):
    """Toggle complaint status"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        booking.has_complaint = not booking.has_complaint
        if not booking.has_complaint:
            booking.complaint_details = ''
        booking.save()
        
        status = 'marked with complaint' if booking.has_complaint else 'marked without complaint'
        messages.success(request, f'Order {status}')
    
    return redirect('booking_detail', pk=pk)


# ============ User Management Views ============

@login_required
def user_list_view(request):
    """List all users"""
    user = request.user
    
    # Only admins and super admins can view user list
    if not (user.is_super_admin() or user.is_admin()):
        messages.error(request, 'You do not have permission to view users')
        return redirect('dashboard')
    
    # Get users based on permissions
    if user.is_super_admin():
        users = CustomUser.objects.all()
    else:
        # Admins can only see technicians
        users = CustomUser.objects.filter(role='technician')
    
    # Apply filters
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    country_filter = request.GET.get('country')
    if country_filter:
        users = users.filter(country=country_filter)
    
    active_filter = request.GET.get('is_active')
    if active_filter == 'true':
        users = users.filter(is_active=True)
    elif active_filter == 'false':
        users = users.filter(is_active=False)
    
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    users = users.order_by('role', 'country', 'last_name')
    
    # Calculate stats
    user_stats = {
        'super_admins': CustomUser.objects.filter(role='super_admin').count() if user.is_super_admin() else 0,
        'admins': CustomUser.objects.filter(role='admin').count(),
        'technicians': CustomUser.objects.filter(role='technician').count(),
        'active_users': CustomUser.objects.filter(is_active=True).count(),
    }
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'user_stats': user_stats,
    }
    
    return render(request, 'user_list.html', context)


@login_required
def user_detail_view(request, pk):
    """User detail view"""
    user = request.user
    view_user = get_object_or_404(CustomUser, pk=pk)
    
    # Check permissions
    if user.role == 'technician' and view_user != user:
        messages.error(request, 'You do not have permission to view other users')
        return redirect('dashboard')
    
    if user.is_admin() and view_user.role != 'technician' and view_user != user:
        messages.error(request, 'You can only view technician profiles')
        return redirect('user_list')
    
    # Get statistics for technicians
    stats = None
    recent_orders = None
    if view_user.role == 'technician':
        orders = Booking.objects.filter(assigned_technician=view_user)
        completed_orders = orders.filter(status='completed')
        stats = {
            'total_orders': orders.count(),
            'completed_orders': completed_orders.count(),
            'in_progress_orders': orders.filter(status='in_progress').count(),
            'orders_with_complaints': completed_orders.filter(has_complaint=True).count(),
            'orders_no_complaints': completed_orders.filter(has_complaint=False).count(),
        }
        recent_orders = orders.order_by('-order_time')[:10]
    
    context = {
        'view_user': view_user,
        'stats': stats,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'user_detail.html', context)


@login_required
def user_create_view(request):
    """Create a new user"""
    user = request.user
    
    # Only admins and super admins can create users
    if not (user.is_super_admin() or user.is_admin()):
        messages.error(request, 'You do not have permission to create users')
        return redirect('user_list')
    
    if request.method == 'POST':
        try:
            role = request.POST.get('role')
            
            # Check permissions
            if role in ['super_admin', 'admin'] and not user.is_super_admin():
                messages.error(request, 'Only super admins can create admin users')
                return redirect('user_list')
            
            # Validate passwords
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            if password != password_confirm:
                messages.error(request, 'Passwords do not match')
                return render(request, 'user_form.html')
            
            # Create user
            new_user = CustomUser.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                password=password,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                role=role,
                phone_number=request.POST.get('phone_number', ''),
                country=request.POST.get('country', ''),
                is_staff=True,
            )
            
            messages.success(request, f'User {new_user.username} created successfully!')
            return redirect('user_detail', pk=new_user.pk)
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'user_form.html')


@login_required
def user_edit_view(request, pk):
    """Edit a user"""
    user = request.user
    view_user = get_object_or_404(CustomUser, pk=pk)
    
    # Check permissions
    if user.role == 'technician':
        messages.error(request, 'You do not have permission to edit users')
        return redirect('dashboard')
    
    if user.is_admin() and view_user.role != 'technician':
        messages.error(request, 'You can only edit technician accounts')
        return redirect('user_list')
    
    if request.method == 'POST':
        try:
            view_user.first_name = request.POST.get('first_name')
            view_user.last_name = request.POST.get('last_name')
            view_user.email = request.POST.get('email')
            view_user.phone_number = request.POST.get('phone_number', '')
            view_user.country = request.POST.get('country', '')
            view_user.is_active = request.POST.get('is_active') == 'on'
            view_user.save()
            
            messages.success(request, f'User {view_user.username} updated successfully!')
            return redirect('user_detail', pk=view_user.pk)
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    context = {
        'view_user': view_user,
    }
    
    return render(request, 'user_form.html', context)


@login_required
def user_delete_view(request, pk):
    """Delete a user"""
    user = request.user
    view_user = get_object_or_404(CustomUser, pk=pk)
    
    # Check permissions
    if view_user == user:
        messages.error(request, 'You cannot delete your own account')
        return redirect('user_detail', pk=pk)
    
    if user.role == 'technician':
        messages.error(request, 'You do not have permission to delete users')
        return redirect('dashboard')
    
    if user.is_admin() and view_user.role != 'technician':
        messages.error(request, 'You can only delete technician accounts')
        return redirect('user_list')
    
    if request.method == 'POST':
        username = view_user.username
        view_user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('user_list')
    
    return redirect('user_detail', pk=pk)


@login_required
def user_toggle_active_view(request, pk):
    """Toggle user active status"""
    user = request.user
    view_user = get_object_or_404(CustomUser, pk=pk)
    
    # Check permissions
    if not (user.is_super_admin() or (user.is_admin() and view_user.role == 'technician')):
        messages.error(request, 'You do not have permission to change user status')
        return redirect('user_detail', pk=pk)
    
    if request.method == 'POST':
        view_user.is_active = not view_user.is_active
        view_user.save()
        
        status = 'activated' if view_user.is_active else 'deactivated'
        messages.success(request, f'User {view_user.username} {status}')
    
    return redirect('user_detail', pk=pk)
    
    return JsonResponse(stats)
