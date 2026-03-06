# 🚀 FUMIGATION SYSTEM - QUICK START

## ⚡ Get Started in 3 Steps

### **Step 1: Setup Database**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### **Step 2: Create Demo Data**
```powershell
python manage.py setup_demo --create-sample-data
```

**This creates:**
- ✅ Admin account (admin / admin123)
- ✅ 5 Technicians across 4 countries (password: tech123)
- ✅ 8 Sample fumigation orders
- ✅ Success tracking examples

### **Step 3: Start Server**
```powershell
python manage.py runserver
```

**Access:** http://127.0.0.1:8000/admin/

---

## 🔑 **Login Credentials**

### **Admin (24/7 Access)**
```
Username: admin
Password: admin123
```

### **Technicians (5 AM - 12 PM Only)**
```
Kenya:         kenya_tech1 / tech123
               kenya_tech2 / tech123
Uganda:        uganda_tech1 / tech123
Zambia:        zambia_tech1 / tech123
South Africa:  sa_tech1 / tech123
```

---

## 🌍 **Countries Supported**
- 🇰🇪 Kenya
- 🇺🇬 Uganda
- 🇿🇲 Zambia
- 🇿🇦 South Africa

---

## 📋 **What Admin Can Do**

### ✅ **Create New Orders (24/7)**
1. Click "Fumigation Orders" → "Add Order"
2. Fill in:
   - **Order Time** - When service is scheduled
   - **Country** - Select from 4 countries
   - **Location Pin** - Google Maps link/coordinates
   - **Client Number** - Phone number
   - **Client Name** - Optional
   - **Amount** - Service charge
3. Click Save

### ✅ **Assign to Technician (Anytime)**
1. Open any order
2. Select **Assigned Technician** (filtered by country)
3. Save
4. Status changes to "Assigned"

### ✅ **Track Success**
After completion, mark orders as:
- ✅ **Successful** - No issues
- ⚠️ **Has Complaint** - Client complained
- 🔄 **Needs Repeat** - Service must be redone

---

## 👨‍🔧 **What Technician Can Do**

### ⏰ **Morning Access Only (5 AM - 12 PM)**
1. Log in during morning hours
2. See only YOUR assigned orders
3. See only orders in YOUR country
4. Update to "In Progress" when starting
5. Update to "Completed" when done
6. Add completion notes

### 🚫 **Outside Morning Hours**
- Access blocked with custom message
- Cannot view or update orders
- Admins can still assign orders anytime

---

## 📊 **Dashboard Shows**

### **For Admin:**
- Total Orders
- Pending / Assigned / In Progress / Completed
- ✅ Successful Orders (no complaints/repeats)
- ⚠️ Orders with Complaints
- 🔄 Orders Needing Repeat
- Total Revenue
- Today's Orders
- Orders by Country (with flags)

### **For Technician:**
- Only their assigned orders
- Orders in their country
- Their daily schedule

---

## 🔄 **Order Flow**

```
Admin Creates Order
      ↓
Admin Assigns to Technician (anytime)
      ↓
Technician Sees Order (morning only)
      ↓
Technician Updates to "In Progress"
      ↓
Technician Completes Service
      ↓
Technician Marks "Completed"
      ↓
Admin Tracks Success/Issues
```

---

## 💡 **Key Features**

### ✅ **Order Information**
- Auto-generated order number (FUMI-2026-00001)
- Order time (appointment)
- Country (4 African countries)
- Location pin (Google Maps)
- Client number & name
- Amount & payment tracking

### ✅ **Assignment System**
- Admin assigns anytime (24/7)
- Technicians grouped by country
- Assignment timestamp tracked
- Order status auto-updates

### ✅ **Success Tracking**
- Mark successful orders (no issues)
- Track complaints with details
- Track repeat services with reasons
- Performance metrics per technician

### ✅ **Time Restrictions**
- Technicians: 5 AM - 12 PM only
- Admins: 24/7 access
- Custom block page outside hours

### ✅ **Country Filtering**
- Technicians see only their country
- Assignment filtered by country
- Dashboard shows country breakdown

---

## 🧪 **Test the System**

### **Test Admin Functions:**
1. Login as `admin`
2. Create a test order
3. Assign to a technician
4. View dashboard statistics

### **Test Technician Access:**
1. **During morning (5 AM - 12 PM):**
   - Login as `kenya_tech1`
   - View assigned orders
   - Update order status

2. **Outside morning hours:**
   - Try logging in as `kenya_tech1`
   - See "Morning Access Only" block page
   - Admin can still login

### **Test Success Tracking:**
1. Complete an order
2. Mark it as:
   - ✅ Successful, OR
   - ⚠️ Has Complaint (add details), OR
   - 🔄 Needs Repeat (add reason)
3. Check dashboard for updated metrics

---

## 🔧 **Common Tasks**

### **Create Custom Admin:**
```powershell
python manage.py createsuperuser
```
Then set role to 'admin' in Django shell:
```python
python manage.py shell
from bookings.models import CustomUser
user = CustomUser.objects.get(username='YOUR_USERNAME')
user.role = 'admin'
user.save()
```

### **Add New Technician:**
1. Login as admin
2. Go to Users → Add User
3. Set Role = "Technician"
4. Set Country = (Kenya/Uganda/Zambia/South Africa)
5. Check "Staff status"
6. Save

### **Reset Demo Data:**
```powershell
del db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py setup_demo --create-sample-data
```

---

## 📖 **Documentation Files**

- **FUMIGATION_README.md** - Complete system documentation
- **SETUP.md** - Original setup guide
- **README.md** - Original booking system docs
- **This file** - Quick start guide

---

## 🚨 **Troubleshooting**

### **"No module named bookings"**
```powershell
python manage.py migrate
```

### **Technician can't login**
- Check current time (must be 5 AM - 12 PM)
- Admin can login anytime

### **Technician sees no orders**
- Check if orders assigned to them
- Check if orders match their country
- Verify technician country field is set

### **Order number not showing**
- Save the order - auto-generates on save

---

## ✨ **You're Ready!**

Your fumigation order management system is now set up with:

✅ Admin portal for order entry (24/7)  
✅ Technician access (morning only)  
✅ 4-country support  
✅ Success tracking  
✅ Performance monitoring  
✅ Country-based assignment  

**Start managing fumigation orders across Africa!** 🦟🌍

---

**Quick Links:**
- Admin Panel: http://127.0.0.1:8000/admin/
- Admin Login: admin / admin123
- Tech Login: kenya_tech1 / tech123 (5 AM - 12 PM)

---

**Need Help?** Check FUMIGATION_README.md for detailed documentation!
