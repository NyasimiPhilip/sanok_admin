# Sanok Admin - Booking Management System

A comprehensive Django-based booking system for pest control services with role-based access control, time restrictions, and an advanced admin dashboard.

## Features

### 📋 Booking Management
- **Complete Booking Information**
  - Time and date scheduling
  - Country/location tracking
  - Contact information (name, email, phone, address)
  - Pest type selection (rodents, cockroaches, termites, etc.)
  - Service amount/pricing
  - Status tracking (Pending, Confirmed, In Progress, Completed, Cancelled)
  
- **Customer Feedback System**
  - Text feedback collection
  - 5-star rating system
  - Service quality tracking

- **Internal Management**
  - Comments and notes for staff
  - Technician assignment
  - Command/instruction tracking

### 👥 User Roles & Permissions

#### Admin Role
- Full system access 24/7
- View and manage all bookings
- Assign technicians to jobs
- Access to dashboard statistics
- User management capabilities

#### Technician Role
- **Limited access hours: 5:00 AM - 6:00 PM only**
- View only assigned bookings
- Update booking status
- Add comments and feedback
- Cannot access other technicians' bookings

### 🕐 Time Restrictions
- Technicians can only access the system between 5:00 AM and 6:00 PM
- Outside these hours, technicians receive a custom access restriction page
- Admins have unrestricted 24/7 access
- Implemented via custom middleware

### 📊 Dashboard Features
- Real-time booking statistics
- Status distribution (Pending, Confirmed, In Progress, Completed, Cancelled)
- Total revenue tracking from completed bookings
- Today's bookings count
- Pest type distribution analytics
- Color-coded status badges
- Rating visualization with stars

### 🔧 Additional Commands System
Special instructions and commands for bookings:
- Reschedule requests
- Special equipment needs
- Access information
- Safety precautions
- Follow-up requirements
- Custom commands

## Installation & Setup

### 1. Database Migration
Run the following commands to set up the database:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 2. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 3. Set Admin Role
After creating the superuser, you need to set their role to 'admin':

```python
# In Django shell
python manage.py shell

from bookings.models import CustomUser
user = CustomUser.objects.get(username='your_username')
user.role = 'admin'
user.save()
```

### 4. Run Development Server
```bash
python manage.py runserver
```

Access the admin panel at: `http://127.0.0.1:8000/admin/`

## Creating Users

### Creating a Technician Account

1. Log in to the admin panel as an admin
2. Navigate to "Users" section
3. Click "Add User"
4. Fill in username and password
5. **Important**: Set the "Role" field to "Technician"
6. Add phone number and other details
7. Save

### User Permissions
- **is_staff**: Must be checked for access to admin panel
- **is_superuser**: Only for admin users
- **role**: Set to 'technician' for limited accounts

## Usage Guide

### For Admins

#### Managing Bookings
1. Go to "Bookings" in the admin panel
2. View dashboard statistics at the top
3. Filter by status, country, or pest type
4. Click on any booking to view/edit details
5. Assign technicians from the booking details page

#### Bulk Actions
- Select multiple bookings using checkboxes
- Use actions dropdown to:
  - Mark as Confirmed
  - Mark as Completed
  - Mark as Cancelled

#### Adding Commands
- Open a booking
- Scroll to "Booking Commands" section
- Add special instructions or notes
- Select command type and description

### For Technicians

#### Access Hours
- Can only log in between 5:00 AM - 6:00 PM
- Attempting access outside these hours shows a restriction message

#### Viewing Assignments
1. Log in to admin panel (during allowed hours)
2. View only bookings assigned to you
3. Update booking status as work progresses
4. Add comments and feedback

## API Endpoints

The system includes JSON API endpoints for statistics:

### Get Booking Statistics
```
GET /api/stats/
```

Returns JSON with:
- Total bookings
- Status breakdown (pending, confirmed, in progress, completed, cancelled)
- Total revenue
- Today's bookings count

**Authentication required** - Statistics filtered by user role

## Models Structure

### CustomUser
- Extends Django's AbstractUser
- Fields: username, email, role, phone_number
- Roles: 'admin' or 'technician'

### Booking
- Complete booking information
- Contact details
- Service details (pest type, amount)
- Status tracking
- Feedback and ratings
- Timestamps and audit trail
- Technician assignment

### BookingCommand
- Related to bookings
- Command type (reschedule, equipment, access, safety, follow-up, other)
- Description and completion status
- Audit trail (created_by, created_at)

## Security Features

1. **Role-Based Access Control (RBAC)**
   - Separate permissions for admin and technician roles
   - Technicians can only view their assigned bookings

2. **Time-Based Access Restrictions**
   - Middleware enforces 5 AM - 6 PM access for technicians
   - Custom error page for out-of-hours access

3. **Audit Trail**
   - Track who created each booking
   - Timestamp all changes
   - Command history with creator information

4. **Data Validation**
   - Email validation
   - Positive amount validation
   - Required fields enforcement

## Customization

### Changing Operating Hours
Edit the time check in `bookings/middleware.py`:
```python
# Change this line to modify hours (currently 5 AM to 6 PM)
if not (5 <= current_hour < 18):
```

### Adding Pest Types
Edit `PEST_CHOICES` in `bookings/models.py`:
```python
PEST_CHOICES = [
    ('rodents', 'Rodents'),
    ('cockroaches', 'Cockroaches'),
    # Add more here
]
```

### Adding Booking Statuses
Edit `STATUS_CHOICES` in `bookings/models.py`:
```python
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    # Add more here
]
```

## Admin Panel Customization

The admin interface includes:
- Custom site header: "Sanok Admin - Booking Management System"
- Color-coded status badges
- Star rating display
- Inline command editing
- Advanced filtering and search
- Dashboard statistics with visual cards

## Troubleshooting

### Issue: Cannot access admin panel
**Solution**: Ensure `is_staff` is checked for the user

### Issue: Technician sees all bookings
**Solution**: Check that user.role is set to 'technician', not 'admin'

### Issue: Time restriction not working
**Solution**: 
1. Verify middleware is in settings.py
2. Check user.role is 'technician'
3. Confirm TIME_ZONE setting matches your location

### Issue: Dashboard stats not showing
**Solution**: Clear browser cache and refresh page

## Technology Stack

- **Framework**: Django 6.0.3
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **Python**: 3.8+
- **Admin Interface**: Django Admin (customized)

## File Structure

```
sanok_admin/
├── manage.py
├── sanok_admin/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── bookings/
    ├── __init__.py
    ├── models.py           # CustomUser, Booking, BookingCommand
    ├── admin.py            # Admin interface customization
    ├── views.py            # Dashboard and API views
    ├── urls.py             # URL routing
    ├── middleware.py       # Time restriction middleware
    ├── migrations/         # Database migrations
    └── templates/
        └── admin/
            └── bookings/
                └── booking/
                    └── change_list.html  # Dashboard template
```

## Future Enhancements

Potential features to add:
- Email notifications for booking confirmations
- SMS alerts for technicians
- Calendar view for bookings
- PDF invoice generation
- Photo upload for pest documentation
- Multiple technician assignment
- Service history tracking
- Payment integration
- Mobile app API
- Reporting and analytics dashboard

## Support

For issues or questions, contact your system administrator.

## License

Proprietary - All rights reserved

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**Developed for**: Sanok Admin Booking System
