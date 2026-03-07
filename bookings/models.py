from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access control
    """
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('technician', 'Technician'),
    ]
    
    COUNTRY_CHOICES = [
        ('kenya', 'Kenya'),
        ('uganda', 'Uganda'),
        ('zambia', 'Zambia'),
        ('south_africa', 'South Africa'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='technician',
        help_text='User role with specific permissions'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(
        max_length=20,
        choices=COUNTRY_CHOICES,
        blank=True,
        help_text='Country where technician operates (for technicians only)'
    )
    
    def is_super_admin(self):
        return self.role == 'super_admin'
    
    def is_admin(self):
        return self.role == 'admin' or self.role == 'super_admin'
    
    def is_technician(self):
        return self.role == 'technician'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        if self.country:
            return f"{self.username} ({self.get_role_display()} - {self.get_country_display()})"
        return f"{self.username} ({self.get_role_display()})"


class Booking(models.Model):
    """
    Fumigation Order/Booking model
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    COUNTRY_CHOICES = [
        ('kenya', 'Kenya'),
        ('uganda', 'Uganda'),
        ('zambia', 'Zambia'),
        ('south_africa', 'South Africa'),
    ]
    
    PEST_CHOICES = [
        ('rodents', 'Rodents'),
        ('cockroaches', 'Cockroaches'),
        ('termites', 'Termites'),
        ('bed_bugs', 'Bed Bugs'),
        ('ants', 'Ants'),
        ('mosquitoes', 'Mosquitoes'),
        ('flies', 'Flies'),
        ('other', 'Other'),
    ]
    
    # Order information
    order_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text='Unique order reference number'
    )
    order_time = models.DateTimeField(
        help_text='Scheduled date and time for fumigation'
    )
    country = models.CharField(
        max_length=20,
        choices=COUNTRY_CHOICES,
        help_text='Country where service is needed'
    )
    
    # Location details
    location_pin = models.CharField(
        max_length=500,
        help_text='Google Maps pin or location coordinates/address'
    )
    location_address = models.TextField(
        help_text='Detailed address or location description'
    )
    
    # Contact information
    client_phone = models.CharField(
        max_length=20,
        help_text='Client phone number'
    )
    
    # Pest type
    pest_type = models.CharField(
        max_length=50,
        choices=PEST_CHOICES,
        help_text='Type of pest problem'
    )
    
    # Financial
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Service charge amount'
    )
    
    # Status and assignment
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    assigned_technician = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'technician'},
        related_name='assigned_orders'
    )
    assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When order was assigned to technician'
    )
    
    # Complaint tracking (Simplified)
    has_complaint = models.BooleanField(
        default=False,
        help_text='Did client complain about service?'
    )
    complaint_details = models.TextField(
        blank=True,
        help_text='Details of client complaint'
    )
    
    # Additional fields
    notes = models.TextField(
        blank=True,
        help_text='Internal notes and comments'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_orders'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When order was completed'
    )
    
    class Meta:
        ordering = ['-order_time']
        verbose_name = 'Fumigation Order'
        verbose_name_plural = 'Fumigation Orders'
        indexes = [
            models.Index(fields=['-order_time']),
            models.Index(fields=['status']),
            models.Index(fields=['country']),
            models.Index(fields=['assigned_technician']),
        ]
    
    def save(self, *args, **kwargs):
        # Auto-generate order number if not provided
        if not self.order_number:
            # Format: FUMI-YYYY-XXXXX
            year = timezone.now().year
            last_order = Booking.objects.filter(
                order_number__startswith=f'FUMI-{year}'
            ).order_by('-order_number').first()
            
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.order_number = f'FUMI-{year}-{new_num:05d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        complaint_status = " ⚠️ COMPLAINT" if self.has_complaint else ""
        return f"Order {self.order_number} - {self.get_country_display()} ({self.get_status_display()}){complaint_status}"
    
    def is_morning_time(self):
        """
        Check if current time is morning (5 AM - 12 PM)
        """
        current_time = timezone.now()
        current_hour = current_time.hour
        return 5 <= current_hour < 12
    
    def get_currency(self):
        """
        Get currency symbol based on country
        """
        currency_map = {
            'kenya': 'KES',
            'uganda': 'UGX',
            'zambia': 'ZMW',
            'south_africa': 'ZAR',
        }
        return currency_map.get(self.country, 'USD')
    
    def get_currency_symbol(self):
        """
        Get currency symbol for display
        """
        symbol_map = {
            'kenya': 'KSh',
            'uganda': 'USh',
            'zambia': 'ZK',
            'south_africa': 'R',
        }
        return symbol_map.get(self.country, '$')
    
    def get_formatted_amount(self):
        """
        Get amount with currency symbol
        """
        return f"{self.get_currency_symbol()} {self.amount:,.2f}"


class BookingCommand(models.Model):
    """
    Additional instructions or notes for fumigation orders
    """
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='instructions'
    )
    instruction_type = models.CharField(
        max_length=100,
        choices=[
            ('equipment', 'Special Equipment Needed'),
            ('access', 'Access Instructions'),
            ('safety', 'Safety Precautions'),
            ('follow_up', 'Follow-up Required'),
            ('client_request', 'Client Special Request'),
            ('other', 'Other'),
        ],
        default='other'
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True
    )
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order Instruction'
        verbose_name_plural = 'Order Instructions'
    
    def __str__(self):
        return f"{self.get_instruction_type_display()} - Order {self.booking.order_number}"
