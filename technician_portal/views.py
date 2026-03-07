from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time
from bookings.models import Booking


def technician_required(view_func):
    """Decorator: only allow technicians."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'role') or request.user.role != 'technician':
            messages.error(request, 'Access denied. Technician account required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@technician_required
def orders_view(request):
    """Technician sees only their assigned orders for today."""
    user = request.user
    today = timezone.now().date()
    start = timezone.make_aware(datetime.combine(today, time(0, 0)))
    end = timezone.make_aware(datetime.combine(today, time(23, 59, 59)))

    orders = Booking.objects.filter(
        assigned_technician=user,
        order_time__gte=start,
        order_time__lte=end,
    ).order_by('order_time')

    return render(request, 'technician_portal/orders.html', {
        'orders': orders,
        'today': today,
    })


@technician_required
def order_detail_view(request, pk):
    """Technician views details of one of their assigned orders."""
    user = request.user
    order = get_object_or_404(Booking, pk=pk)

    if order.assigned_technician != user:
        messages.error(request, 'You are not assigned to this order.')
        return redirect('technician:orders')

    return render(request, 'technician_portal/order_detail.html', {'order': order})


@technician_required
def update_status_view(request, pk):
    """Technician updates the status of their assigned order."""
    user = request.user
    order = get_object_or_404(Booking, pk=pk)

    if order.assigned_technician != user:
        messages.error(request, 'You are not assigned to this order.')
        return redirect('technician:orders')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        allowed = ['in_progress', 'completed']
        if new_status in allowed:
            order.status = new_status
            if new_status == 'completed':
                order.completed_at = timezone.now()
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('technician:order_detail', pk=pk)
