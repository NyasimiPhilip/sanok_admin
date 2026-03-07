from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from bookings.models import Booking, CustomUser


def super_admin_required(view_func):
    """Decorator: only allow super_admin role."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role != 'super_admin':
            messages.error(request, 'Access denied. Super Admin account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@super_admin_required
def dashboard_view(request):
    orders = Booking.objects.all()
    stats = {
        'total_orders': orders.count(),
        'pending': orders.filter(status='pending').count(),
        'completed': orders.filter(status='completed').count(),
        'with_complaints': orders.filter(has_complaint=True).count(),
        'total_admins': CustomUser.objects.filter(role='admin').count(),
        'total_technicians': CustomUser.objects.filter(role='technician').count(),
    }
    recent = orders.order_by('-order_time')[:10]
    return render(request, 'super_admin_portal/dashboard.html', {
        'stats': stats,
        'recent': recent,
    })


# -------- User Management --------

@super_admin_required
def user_list_view(request):
    role_f = request.GET.get('role', '')
    users = CustomUser.objects.exclude(role='super_admin').order_by('role', 'last_name')
    if role_f:
        users = users.filter(role=role_f)

    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    return render(request, 'super_admin_portal/user_list.html', {'users': users})


@super_admin_required
def user_create_view(request):
    if request.method == 'POST':
        try:
            role = request.POST.get('role')
            if role not in ('admin', 'technician'):
                messages.error(request, 'Invalid role.')
                return redirect('super_admin:user_create')

            password = request.POST.get('password')
            if password != request.POST.get('password_confirm'):
                messages.error(request, 'Passwords do not match.')
                return render(request, 'super_admin_portal/user_form.html')

            new_user = CustomUser.objects.create_user(
                username=request.POST.get('username'),
                email=request.POST.get('email', ''),
                password=password,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                role=role,
                phone_number=request.POST.get('phone_number', ''),
                country=request.POST.get('country', ''),
                is_staff=(role == 'admin'),
            )
            messages.success(request, f'User {new_user.username} created.')
            return redirect('super_admin:user_list')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'super_admin_portal/user_form.html')


@super_admin_required
def user_edit_view(request, pk):
    target = get_object_or_404(CustomUser, pk=pk)
    if target.role == 'super_admin':
        messages.error(request, 'Cannot edit another super admin.')
        return redirect('super_admin:user_list')

    if request.method == 'POST':
        try:
            role = request.POST.get('role')
            if role not in ('admin', 'technician'):
                messages.error(request, 'Invalid role.')
                return render(request, 'super_admin_portal/user_form.html', {'target': target})

            target.username = request.POST.get('username', '').strip()
            target.role = role
            target.first_name = request.POST.get('first_name', '')
            target.last_name = request.POST.get('last_name', '')
            target.email = request.POST.get('email', '')
            target.phone_number = request.POST.get('phone_number', '')
            target.country = request.POST.get('country', '')
            target.is_active = request.POST.get('is_active') == 'on'
            target.is_staff = role == 'admin'
            target.is_superuser = False
            new_pw = request.POST.get('password')
            if new_pw:
                target.set_password(new_pw)
            target.save()
            messages.success(request, f'User {target.username} updated.')
            return redirect('super_admin:user_list')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'super_admin_portal/user_form.html', {'target': target})


@super_admin_required
def user_delete_view(request, pk):
    target = get_object_or_404(CustomUser, pk=pk)
    if target.role == 'super_admin':
        messages.error(request, 'Cannot delete a super admin.')
        return redirect('super_admin:user_list')
    if request.method == 'POST':
        uname = target.username
        target.delete()
        messages.success(request, f'User {uname} deleted.')
        return redirect('super_admin:user_list')
    return redirect('super_admin:user_list')


@super_admin_required
def user_toggle_active_view(request, pk):
    target = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        target.is_active = not target.is_active
        target.save()
        state = 'activated' if target.is_active else 'deactivated'
        messages.success(request, f'User {target.username} {state}.')
    return redirect('super_admin:user_list')


# -------- Orders (read-only overview) --------

@super_admin_required
def order_list_view(request):
    orders = Booking.objects.all().order_by('-order_time')

    status_f = request.GET.get('status')
    if status_f:
        orders = orders.filter(status=status_f)

    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(client_phone__icontains=search) |
            Q(location_address__icontains=search)
        )

    return render(request, 'super_admin_portal/order_list.html', {'orders': orders})
