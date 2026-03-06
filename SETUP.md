# 🚀 Sanok Admin - ONE-COMMAND SETUP

## The Fastest Way to Get Started

### Step 1: Run Migrations
```powershell
python manage.py makemigrations; python manage.py migrate
```

### Step 2: Setup Demo Data (Includes Admin + Sample Bookings)
```powershell
python manage.py setup_demo --create-sample-data
```

This single command will:
- ✅ Create admin user (username: `admin`, password: `admin123`)
- ✅ Create 2 technician accounts (john_tech & sarah_tech, password: `tech123`)
- ✅ Create 8 sample bookings with various statuses
- ✅ Add booking commands and feedback

### Step 3: Start Server
```powershell
python manage.py runserver
```

### Step 4: Login
Open browser: **http://127.0.0.1:8000/admin/**

**Admin Login:**
- Username: `admin`
- Password: `admin123`

**Technician Login (5 AM - 6 PM only):**
- Username: `john_tech` or `sarah_tech`
- Password: `tech123`

---

## 🎯 That's It! Your System is Ready!

### What You Can Do Now:

#### As Admin:
1. View dashboard with statistics
2. See all 8 sample bookings
3. Filter by status, country, or pest type
4. Assign bookings to technicians
5. Add new bookings
6. Manage users

#### As Technician (during 5 AM - 6 PM):
1. View only assigned bookings
2. Update booking status
3. Add comments
4. See booking commands

---

## 🔧 Custom Setup Options

### Just Create Admin (No Sample Data)
```powershell
python manage.py setup_demo
```

### Custom Admin Credentials
```powershell
python manage.py setup_demo --admin-username=myusername --admin-password=mypassword --create-sample-data
```

---

## 📊 What You'll See

After setup, your admin dashboard will show:
- **8 Total Bookings**
- Mix of statuses (pending, confirmed, in progress, completed)
- Revenue from completed bookings
- Today's bookings
- Full booking details with:
  - Customer contact information
  - Pest types
  - Amounts
  - Ratings and feedback (for completed)
  - Special commands

---

## 🧪 Test Features

### Test Time Restriction:
1. Log out from admin
2. If current time is **after 6 PM or before 5 AM**:
   - Try logging in as `john_tech`
   - You'll see "Access Restricted" page
3. Admin can login anytime

### Test Technician View:
1. Login as `john_tech` (during allowed hours)
2. You'll only see bookings assigned to John
3. Cannot see Sarah's bookings

### Test Admin Features:
1. Login as `admin`
2. See ALL bookings
3. Try bulk actions (select multiple bookings):
   - Mark as Confirmed
   - Mark as Completed
   - Mark as Cancelled

---

## 📁 Project Structure Created

```
sanok_admin/
├── manage.py
├── requirements.txt
├── README.md (Full documentation)
├── QUICKSTART.md (Detailed guide)
├── SETUP.md (This file)
├── db.sqlite3 (Created after migrations)
├── sanok_admin/
│   ├── settings.py (✅ Configured)
│   ├── urls.py (✅ Configured)
│   └── ...
└── bookings/
    ├── models.py (✅ CustomUser, Booking, BookingCommand)
    ├── admin.py (✅ Dashboard with stats)
    ├── views.py (✅ Views and API)
    ├── urls.py (✅ URL routing)
    ├── middleware.py (✅ Time restrictions)
    ├── management/
    │   └── commands/
    │       └── setup_demo.py (✅ Setup script)
    └── templates/
        └── admin/ (✅ Dashboard template)
```

---

## 🎨 Features Included

### ✅ Booking Management
- Complete booking information (time, country, contact, pests, amount)
- Status tracking (pending → confirmed → in progress → completed)
- Customer feedback with 5-star ratings
- Internal comments and notes

### ✅ User Roles
- **Admin**: Full access 24/7
- **Technician**: Limited access (5 AM - 6 PM), only see assigned bookings

### ✅ Dashboard
- Real-time statistics
- Status distribution
- Revenue tracking
- Today's bookings count
- Color-coded status badges

### ✅ Additional Commands
- Special instructions for bookings
- Equipment needs
- Access information
- Safety precautions
- Follow-up tasks

### ✅ Time Restrictions
- Middleware enforces technician access hours
- Custom error page for out-of-hours access
- Admins bypass restrictions

### ✅ API Endpoints
- `/api/stats/` - Get booking statistics as JSON

---

## 🆘 Quick Troubleshooting

### "No module named bookings"
```powershell
# Make sure you're in the right directory
cd c:\Users\Nyasimi\Documents\sanok_admin
python manage.py check
```

### "Table doesn't exist"
```powershell
# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### "Cannot login"
```powershell
# Reset admin password
python manage.py changepassword admin
```

### "Dashboard stats not showing"
- Clear browser cache (Ctrl + Shift + Delete)
- Make sure you're viewing the Bookings list page
- Refresh page (Ctrl + F5)

---

## 🔄 Reset Everything (Start Fresh)

```powershell
# Delete database
del db.sqlite3

# Delete old migrations
rmdir /s bookings\migrations

# Recreate everything
python manage.py makemigrations bookings
python manage.py migrate
python manage.py setup_demo --create-sample-data
```

---

## 📞 Need Help?

Check the documentation:
- **README.md** - Complete system documentation
- **QUICKSTART.md** - Detailed setup guide
- **SETUP.md** - This file

---

## 🎉 You're All Set!

Your booking management system is ready to use with:
- ✅ Database configured
- ✅ Admin account created
- ✅ Sample data loaded
- ✅ Time restrictions active
- ✅ Dashboard ready

**Start managing bookings now!** 🚀

---

**Version**: 1.0.0  
**Created**: March 2026  
**Framework**: Django 6.0.3
