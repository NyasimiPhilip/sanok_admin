from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime
from bookings.models import Booking, CustomUser


def admin_required(view_func):
    """Decorator: allow admin and super_admin roles."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role not in ('admin', 'super_admin'):
            messages.error(request, 'Access denied. Admin account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard_view(request):
    orders = Booking.objects.all()
    stats = {
        'total': orders.count(),
        'pending': orders.filter(status='pending').count(),
        'assigned': orders.filter(status='assigned').count(),
        'completed': orders.filter(status='completed').count(),
        'with_complaints': orders.filter(has_complaint=True).count(),
    }
    recent = orders.order_by('-order_time')[:10]
    return render(request, 'admin_portal/dashboard.html', {'stats': stats, 'recent': recent})


@admin_required
def order_list_view(request):
    orders = Booking.objects.all().order_by('-order_time')

    status_f = request.GET.get('status')
    if status_f:
        orders = orders.filter(status=status_f)

    country_f = request.GET.get('country')
    if country_f:
        orders = orders.filter(country=country_f)

    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(client_phone__icontains=search) |
            Q(location_address__icontains=search)
        )

    technicians = CustomUser.objects.filter(role='technician', is_active=True)
    return render(request, 'admin_portal/order_list.html', {
        'orders': orders,
        'technicians': technicians,
    })


@admin_required
def order_detail_view(request, pk):
    order = get_object_or_404(Booking, pk=pk)
    technicians = CustomUser.objects.filter(role='technician', is_active=True)
    return render(request, 'admin_portal/order_detail.html', {
        'order': order,
        'technicians': technicians,
    })


@admin_required
def order_create_view(request):
    if request.method == 'POST':
        try:
            order = Booking.objects.create(
                order_time=datetime.fromisoformat(request.POST.get('order_time')),
                country=request.POST.get('country'),
                location_pin=request.POST.get('location_pin'),
                location_address=request.POST.get('location_address'),
                client_phone=request.POST.get('client_phone'),
                pest_type=request.POST.get('pest_type'),
                amount=float(request.POST.get('amount')),
                notes=request.POST.get('notes', ''),
                status='pending',
                created_by=request.user,
            )
            tech_id = request.POST.get('assigned_technician')
            if tech_id:
                tech = get_object_or_404(CustomUser, pk=tech_id, role='technician')
                order.assigned_technician = tech
                order.assigned_at = timezone.now()
                order.status = 'assigned'
                order.save()
            messages.success(request, f'Order {order.order_number} created successfully.')
            return redirect('admin_portal:order_detail', pk=order.pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    technicians = CustomUser.objects.filter(role='technician', is_active=True)
    return render(request, 'admin_portal/order_form.html', {'technicians': technicians})


@admin_required
def order_edit_view(request, pk):
    order = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        try:
            order.order_time = datetime.fromisoformat(request.POST.get('order_time'))
            order.country = request.POST.get('country')
            order.location_pin = request.POST.get('location_pin')
            order.location_address = request.POST.get('location_address')
            order.client_phone = request.POST.get('client_phone')
            order.pest_type = request.POST.get('pest_type')
            order.amount = float(request.POST.get('amount'))
            order.status = request.POST.get('status')
            order.notes = request.POST.get('notes', '')
            order.has_complaint = request.POST.get('has_complaint') == 'on'
            order.complaint_details = request.POST.get('complaint_details', '')

            tech_id = request.POST.get('assigned_technician')
            if tech_id:
                tech = get_object_or_404(CustomUser, pk=tech_id, role='technician')
                if order.assigned_technician != tech:
                    order.assigned_technician = tech
                    order.assigned_at = timezone.now()
            else:
                order.assigned_technician = None
                order.assigned_at = None

            order.save()
            messages.success(request, f'Order {order.order_number} updated.')
            return redirect('admin_portal:order_detail', pk=order.pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    technicians = CustomUser.objects.filter(role='technician', is_active=True)
    return render(request, 'admin_portal/order_form.html', {
        'order': order,
        'technicians': technicians,
    })


@admin_required
def order_delete_view(request, pk):
    order = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        num = order.order_number
        order.delete()
        messages.success(request, f'Order {num} deleted.')
        return redirect('admin_portal:order_list')
    return redirect('admin_portal:order_detail', pk=pk)


@admin_required
def assign_technician_view(request, pk):
    order = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        tech_id = request.POST.get('technician')
        if tech_id:
            tech = get_object_or_404(CustomUser, pk=tech_id, role='technician')
            order.assigned_technician = tech
            order.assigned_at = timezone.now()
            if order.status == 'pending':
                order.status = 'assigned'
            order.save()
            messages.success(request, f'Order assigned to {tech.get_full_name()}.')
        else:
            order.assigned_technician = None
            order.assigned_at = None
            order.status = 'pending'
            order.save()
            messages.success(request, 'Technician unassigned.')
    return redirect('admin_portal:order_detail', pk=pk)


@admin_required
def technician_list_view(request):
    technicians = CustomUser.objects.filter(role='technician').order_by('last_name')
    return render(request, 'admin_portal/technician_list.html', {'technicians': technicians})
