# Sanok Admin - Quick Setup Guide

## Quick Start (5 minutes)

### Step 1: Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Admin User
```bash
python manage.py createsuperuser
```
- Username: admin (or your choice)
- Email: admin@example.com
- Password: (choose a strong password)

### Step 3: Set Admin Role
```bash
python manage.py shell
```
Then in the Python shell:
```python
from bookings.models import CustomUser
user = CustomUser.objects.get(username='admin')  # Replace 'admin' with your username
user.role = 'admin'
user.save()
exit()
```

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Access Admin Panel
Open your browser: `http://127.0.0.1:8000/admin/`

---

## Creating a Technician Account

### Option 1: Via Admin Panel (Recommended)
1. Log in as admin
2. Go to Users → Add User
3. Create username and password
4. **Set Role to "Technician"**
5. Check "Staff status" box
6. Save

### Option 2: Via Shell
```bash
python manage.py shell
```
```python
from bookings.models import CustomUser
tech = CustomUser.objects.create_user(
    username='technician1',
    email='tech1@example.com',
    password='password123',
    role='technician',
    is_staff=True
)
print(f"Technician created: {tech.username}")
exit()
```

---

## Testing the System

### Test Booking Creation
1. Log in as admin
2. Go to Bookings → Add Booking
3. Fill in:
   - Booking time: (select date/time)
   - Country: United States
   - Contact name: John Doe
   - Contact email: john@example.com
   - Contact phone: +1234567890
   - Contact address: 123 Main St
   - Pests: Rodents
   - Amount: 150.00
   - Status: Pending
4. Save

### Test Technician Assignment
1. Open the booking you created
2. Select assigned technician
3. Save

### Test Technician Login
1. Log out from admin
2. Log in as technician (during 5 AM - 6 PM hours)
3. Verify you only see assigned bookings

### Test Time Restriction
1. If current time is before 5 AM or after 6 PM:
   - Try to log in as technician
   - You should see the access restriction page
2. Log in as admin works at any time

---

## Common Commands

### Reset Database (Start Fresh)
```bash
del db.sqlite3
rmdir /s bookings\migrations
python manage.py makemigrations bookings
python manage.py migrate
python manage.py createsuperuser
```

### Check for Errors
```bash
python manage.py check
```

### Run Tests
```bash
python manage.py test bookings
```

### Create Sample Data
```bash
python manage.py shell
```
```python
from bookings.models import CustomUser, Booking
from django.utils import timezone
from datetime import timedelta

# Create technician
tech = CustomUser.objects.create_user(
    username='tech1',
    password='tech123',
    role='technician',
    is_staff=True,
    first_name='John',
    last_name='Smith'
)

# Create sample bookings
for i in range(5):
    Booking.objects.create(
        booking_time=timezone.now() + timedelta(days=i),
        country='United States',
        contact_name=f'Customer {i+1}',
        contact_email=f'customer{i+1}@example.com',
        contact_phone=f'+123456789{i}',
        contact_address=f'{100+i} Main Street',
        pests='rodents',
        amount=100 + (i * 25),
        status='pending',
        assigned_technician=tech
    )

print("Sample data created!")
exit()
```

---

## API Testing

### Get Statistics (JSON)
```bash
# Windows CMD/PowerShell (logged in)
curl http://127.0.0.1:8000/api/stats/
```

Or visit in browser: `http://127.0.0.1:8000/api/stats/`

---

## Troubleshooting

### "No module named bookings"
- Make sure you're in the correct directory
- Run: `python manage.py migrate`

### "Cannot log in"
- Verify `is_staff=True` for the user
- Check password is correct
- Ensure migrations are applied

### "Access restricted" for admin
- Check user.role is set to 'admin'
- Verify in shell: `CustomUser.objects.get(username='admin').role`

### Dashboard stats not showing
- Ensure you're viewing the Bookings list page
- Clear browser cache
- Check template file exists

---

## System Information

**Admin Access**: 24/7 unrestricted  
**Technician Access**: 5:00 AM - 6:00 PM only  

**Admin Panel**: http://127.0.0.1:8000/admin/  
**API Stats**: http://127.0.0.1:8000/api/stats/

---

## Security Notes

- Change SECRET_KEY in production
- Set DEBUG=False in production
- Use strong passwords
- Restrict ALLOWED_HOSTS in production
- Use environment variables for sensitive data
- Consider PostgreSQL for production

---

Ready to use! 🚀
