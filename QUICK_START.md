# Quick Start - Sanok Fumigation SSR Application

## 🚀 Getting Started in 5 Minutes

### Step 1: Migrate Database
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Demo Data
```powershell
python manage.py setup_demo --create-sample-data
```

### Step 3: Start Server
```powershell
python manage.py runserver
```

### Step 4: Login
Open browser to http://127.0.0.1:8000/

**Login as Super Admin:**
- Username: `superadmin`
- Password: `super123`

**OR Login as Admin:**
- Username: `admin`
- Password: `admin123`

**OR Login as Technician (5 AM - 12 PM only):**
- Username: `kenya_tech1`, `uganda_tech1`, etc.
- Password: `tech123`

## 🎯 What You Can Do

### As Super Admin or Admin:
1. **View Dashboard** - See all statistics and orders
2. **Create Orders** - Click "New Order" button
3. **Manage Users** - Click "Users" in navigation
4. **View/Edit Orders** - Click on any order to see details

### As Technician:
1. **View Dashboard** - See your assigned orders
2. **Today's Schedule** - Check orders for today
3. **Update Status** - Mark orders as in progress or completed
4. **Morning Access Only** - Login between 5 AM - 12 PM

## 📋 Common Tasks

### Create a New Order (Admin/Super Admin)
1. Click "New Order" or go to `/bookings/create/`
2. Fill in:
   - Date & Time
   - Country
   - Location (Google Maps link + address)
   - Client phone
   - Pest type
   - Amount
3. Optionally assign a technician
4. Click "Create Order"

### Manage Users (Admin/Super Admin)
1. Go to "Users" in navigation
2. Click "+ Add User"
3. Fill in details:
   - Choose role (Super Admin can create Admins)
   - Enter username, password, name, email
   - Select country (for technicians)
4. Click "Create User"

### Update Order Status (Any Role)
1. Open order details
2. Click appropriate action button:
   - "Mark as Assigned"
   - "Mark as In Progress"
   - "Mark as Completed"

### Track Complaints
1. View order details
2. Click "Mark as Complained" if client complains
3. Add complaint details
4. Or click "Mark as No Complaint" to clear

## 🗺️ Navigation Map

```
Login Page (/)
    ↓
Dashboard (/dashboard/)
    ├── Orders (/bookings/)
    │   ├── Order Details (/bookings/<id>/)
    │   ├── Create Order (/bookings/create/) [Admin only]
    │   └── Edit Order (/bookings/<id>/edit/) [Admin only]
    │
    ├── Users (/users/) [Admin/Super Admin only]
    │   ├── User Profile (/users/<id>/)
    │   ├── Create User (/users/create/)
    │   └── Edit User (/users/<id>/edit/)
    │
    ├── Home (/home/)
    └── Admin Panel (/admin/)
```

## 🎨 UI Elements Guide

### Status Badges
- 🟡 **Pending** - Just created
- 🔵 **Assigned** - Technician assigned
- 🔵 **In Progress** - Work ongoing
- 🟢 **Completed** - Finished
- 🔴 **Cancelled** - Cancelled

### Complaint Indicators
- ✅ **Green Checkmark** - No complaints
- ⚠️ **Red Warning** - Has complaint

### Role Badges
- 🟣 **Super Admin** - Purple gradient
- 🔴 **Admin** - Pink/red gradient
- 🔵 **Technician** - Blue gradient

## ⚡ Keyboard Shortcuts (Browser)
- `Ctrl + F` - Search within page
- `F5` - Refresh page
- `Alt + ←` - Go back

## 🐛 Troubleshooting

### Can't Login as Technician
- **Problem**: "Technicians can only access between 5 AM - 12 PM"
- **Solution**: Wait until morning hours OR temporarily disable time check in middleware

### Orders Not Showing
- **Problem**: Empty order list
- **Solution**: Run `python manage.py setup_demo --create-sample-data`

### Permission Denied
- **Problem**: "You do not have permission"
- **Solution**: Login with appropriate role (Admin/Super Admin)

### Forgot Password
- **Solution**: Use Django admin to reset:
  ```powershell
  python manage.py changepassword username
  ```

## 📊 Dashboard Statistics Explained

### Total Orders
Count of all orders in the system (or assigned to you as technician)

### Status Counts
- **Pending**: Not yet assigned
- **Assigned**: Technician assigned but not started
- **In Progress**: Work ongoing
- **Completed**: Finished services

### Complaint Tracking
- **With Complaints**: Client reported issues
- **No Complaints**: Successful service

### Total Revenue
Sum of all completed order amounts

### Country Stats
Number of orders per country (Kenya, Uganda, Zambia, South Africa)

## 🔐 Access Control Summary

| Feature | Super Admin | Admin | Technician |
|---------|------------|-------|------------|
| View Dashboard | ✅ | ✅ | ✅ |
| Create Orders | ✅ | ✅ | ❌ |
| Edit Orders | ✅ | ✅ | ❌ |
| View All Orders | ✅ | ✅ | Own Only |
| Create Admins | ✅ | ❌ | ❌ |
| Create Technicians | ✅ | ✅ | ❌ |
| Delete Users | ✅ | Tech Only | ❌ |
| 24/7 Access | ✅ | ✅ | ❌ (5AM-12PM) |

## 📱 Mobile Usage

The application is fully responsive. On mobile:
- Navigation becomes compact
- Tables scroll horizontally
- Forms stack vertically
- Buttons remain touch-friendly

## 🎯 Best Practices

1. **Create Orders Early**: Admins should create orders in advance
2. **Assign by Country**: Assign technicians to their country for efficiency
3. **Morning Planning**: Technicians should check dashboard each morning
4. **Track Complaints**: Always mark complaint status for quality tracking
5. **Update Status**: Keep order status current for accurate reporting

## ⏱️ Time Check

Current restrictions:
- **Technicians**: 5:00 AM - 12:00 PM local server time
- **Admins/Super Admins**: Anytime

To check server time:
```python
from django.utils import timezone
print(timezone.now())
```

## 🔄 Workflow Example

### Standard Order Flow:
1. **Admin** creates order → Status: Pending
2. **Admin** assigns technician → Status: Assigned
3. **Technician** starts work → Status: In Progress
4. **Technician** completes → Status: Completed
5. **Admin** marks complaint status (if any)

## 📞 Need Help?
- Check [SSR_APPLICATION_GUIDE.md](./SSR_APPLICATION_GUIDE.md) for detailed documentation
- Review Django admin logs
- Check browser console for client-side errors
- Review server terminal for backend errors

---

**Ready to start?** Run the setup commands and login! 🚀
