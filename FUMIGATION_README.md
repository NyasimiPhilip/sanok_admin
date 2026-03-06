# 🦟 Sanok Fumigation - Order Management System

A comprehensive Django-based order management system specifically designed for fumigation companies operating across multiple African countries with role-based access control and time-restricted technician access.

---

## 🌍 **System Overview**

This backend system manages fumigation orders across **4 countries**:
- 🇰🇪 **Kenya**
- 🇺🇬 **Uganda**
- 🇿🇲 **Zambia**
- 🇿🇦 **South Africa**

---

## 👥 **User Roles & Access**

### **Admin**
- ✅ **Full 24/7 access** - Can work anytime
- ✅ Input new orders as they come in
- ✅ Assign orders to technicians at any time
- ✅ Track technician performance (successful orders)
- ✅ View all orders across all countries
- ✅ Monitor complaints and repeat services

### **Technician**
- ⏰ **Morning access only** (5:00 AM - 12:00 PM)
- 🗺️ **Country-specific** - Grouped by assigned country
- 👁️ **Limited view** - See only orders assigned to them
- 📝 Can update order status and add completion notes
- 🚫 Cannot see other technicians' orders

---

## 📋 **Order Fields**

When admin inputs a new order, these fields are captured:

| Field | Description | Required |
|-------|-------------|----------|
| **Order Number** | Auto-generated (FUMI-YYYY-XXXXX) | Auto |
| **Order Time** | Scheduled date & time for fumigation | ✅ Yes |
| **Country** | Kenya, Uganda, Zambia, or South Africa | ✅ Yes |
| **Location Pin** | Google Maps link or coordinates | ✅ Yes |
| **Location Address** | Detailed address description | Optional |
| **Client Number** | Client phone number | ✅ Yes |
| **Client Name** | Client full name | Optional |
| **Amount** | Service charge | ✅ Yes |
| **Amount Paid** | Payment received | Auto (0) |
| **Assigned Technician** | Technician for the job | Optional |
| **Notes** | Internal notes | Optional |

---

## ✅ **Success Tracking System**

The admin can track technician performance through:

### **Successful Orders** ✅
Orders completed with:
- ✅ No complaints from client
- ✅ No repeat service needed
- ✅ Job done right the first time

### **Orders with Issues** ⚠️
- **Complaints** - Client reported problems
- **Repeats** - Service needs to be redone
- **Completion notes** - Technician feedback

### **Performance Metrics**
Dashboard shows:
- Total successful orders
- Orders with complaints
- Orders needing repeat service
- Success rate per technician

---

## 🕐 **Access Control**

### **Admin Assignment Workflow**
```
1. Admin receives customer call (anytime)
2. Admin creates order in system (24/7 access)
3. Admin assigns order to technician based on country
4. Assignment timestamp recorded
5. Order status changes to "Assigned"
```

### **Technician View Workflow**
```
1. Technician logs in during morning hours (5 AM - 12 PM)
2. Sees only their assigned orders
3. Views orders filtered by their country
4. Updates order progress
5. Adds completion notes after service
```

### **Outside Morning Hours**
- Technicians attempting to log in outside 5 AM - 12 PM see:
  - Custom access restriction page
  - Current time display
  - Message about morning-only access
  - Note that admins assign orders throughout the day

---

## 🚀 **Quick Setup**

### **1. Run Migrations**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### **2. Create Demo Data**
```powershell
python manage.py setup_demo --create-sample-data
```

This creates:
- ✅ Admin account (admin / admin123)
- ✅ 5 Technicians (one for each country + extra for Kenya)
- ✅ 8 Sample orders across all countries
- ✅ Success tracking examples (successful, complaints, repeats)

### **3. Start Server**
```powershell
python manage.py runserver
```

### **4. Login**
Open: **http://127.0.0.1:8000/admin/**

---

## 👤 **Default User Accounts**

### **Admin**
```
Username: admin
Password: admin123
Access: 24/7
```

### **Technicians** (Password for all: `tech123`)

| Username | Country | Phone | Access Hours |
|----------|---------|-------|--------------|
| kenya_tech1 | 🇰🇪 Kenya | +254-700-123456 | 5 AM - 12 PM |
| kenya_tech2 | 🇰🇪 Kenya | +254-700-123457 | 5 AM - 12 PM |
| uganda_tech1 | 🇺🇬 Uganda | +256-700-123456 | 5 AM - 12 PM |
| zambia_tech1 | 🇿🇲 Zambia | +260-97-1234567 | 5 AM - 12 PM |
| sa_tech1 | 🇿🇦 South Africa | +27-82-1234567 | 5 AM - 12 PM |

---

## 📊 **Dashboard Features**

### **Admin Dashboard Shows:**
1. **Total Orders** - All orders in system
2. **Pending** - Not yet assigned
3. **Assigned** - Assigned to technician
4. **In Progress** - Currently being serviced
5. **Completed** - Finished jobs
6. **✅ Successful Orders** - No complaints/repeats
7. **⚠️ Complaints** - Orders with client complaints
8. **🔄 Repeats** - Orders needing repeat service
9. **Total Revenue** - Sum of completed orders
10. **Today's Orders** - Orders scheduled for today
11. **Orders by Country** - Breakdown with flags

### **Technician Dashboard Shows:**
- Only their assigned orders
- Orders in their country
- Their performance metrics
- Orders scheduled for today

---

## 📱 **Admin Operations**

### **Creating a New Order**
1. Go to **Fumigation Orders** → **Add Order**
2. Fill in:
   - Order time (when service is scheduled)
   - Country (Kenya, Uganda, Zambia, South Africa)
   - Location pin (Google Maps link)
   - Client number (phone)
   - Client name
   - Amount (service charge)
3. Optionally assign technician immediately
4. Add any special instructions
5. Save

### **Assigning Orders**
1. Open the order
2. Select **Assigned Technician** from dropdown
   - Dropdown shows only technicians from that country
3. Save
4. Status automatically changes to "Assigned"
5. Assignment timestamp recorded

### **Tracking Success**
After order completion:
1. Open completed order
2. Check **Success Tracking** section:
   - ✅ Mark as **Successful** if no issues
   - ⚠️ Mark **Has Complaint** if client complained
   - Add **Complaint Details**
   - 🔄 Mark **Is Repeat** if service needs redoing
   - Add **Repeat Reason**
3. Save

### **Bulk Actions**
Select multiple orders and:
- Mark as Completed
- Mark as Successful
- Mark as Having Issues

---

## 🔧 **Technician Operations**

### **Viewing Assigned Orders** (Morning Only)
1. Log in between 5:00 AM - 12:00 PM
2. See dashboard with orders
3. View only orders assigned to you
4. Orders filtered by your country

### **Updating Order Status**
1. Click on your order
2. Change **Status**:
   - Assigned → In Progress (when you start)
   - In Progress → Completed (when done)
3. Add **Completion Notes** with details
4. Save

### **Adding Instructions**
Technicians can add notes about:
- Equipment used
- Service completed
- Client feedback
- Follow-up needs

---

## 🎯 **Order Status Flow**

```
Pending → Assigned → In Progress → Completed
  ↓         ↓            ↓            ↓
Admin   Assignment  Technician   Tracking
Creates  Technician  Starts      Success/
        to Order    Service     Issues
```

---

## 🗺️ **Country-Based Filtering**

### **How It Works:**
1. Each technician is assigned a **home country**
2. Admin assigns orders based on customer location
3. Technicians see only orders from their country
4. Dashboard shows country breakdown with flags

### **Example:**
- **Kenya Technician** sees only Kenya 🇰🇪 orders
- **Uganda Technician** sees only Uganda 🇺🇬 orders
- **Admin** sees all orders from all countries

---

## 📈 **Performance Tracking**

### **Success Metrics**
```
Successful Order = Completed + No Complaints + No Repeats
```

### **Admin Can Track:**
- ✅ Total successful orders per technician
- ⚠️ Orders with complaints (needs attention)
- 🔄 Orders needing repeat (quality issue)
- Success rate percentage
- Revenue from completed orders
- Payment status (paid vs balance)

### **Visual Indicators**
- ✅ Green checkmark = Successful
- ⚠️ Warning symbol = Has complaint  
- 🔄 Repeat symbol = Needs repeat service
- ⚡ Lightning = Check status

---

## 🔐 **Security Features**

1. **Role-Based Access Control**
   - Admin vs Technician permissions
   - Country-based filtering for technicians

2. **Time-Based Access**
   - Middleware enforces morning-only for technicians
   - Custom block page for unauthorized times

3. **Data Privacy**
   - Technicians can't see other technicians' orders
   - Country-specific data isolation

4. **Audit Trail**
   - Track who created each order
   - Assignment timestamps
   - Completion timestamps
   - Update history

---

## 🛠️ **Advanced Features**

### **Order Instructions**
Add special notes for orders:
- Equipment needed
- Access instructions (gate codes, etc.)
- Safety precautions
- Client special requests
- Follow-up requirements

### **Payment Tracking**
- Track **Amount** (total charge)
- Track **Amount Paid** (received payment)
- Automatically calculate **Balance**
- Flag **Fully Paid** orders

### **Auto-Generated Order Numbers**
Format: `FUMI-2026-00001`
- FUMI = Fumigation
- 2026 = Year
- 00001 = Sequential number

---

## 📞 **Common Workflows**

### **Workflow 1: New Customer Call**
```
1. Customer calls admin requesting fumigation
2. Admin logs into system (any time of day)
3. Admin creates new order:
   - Enters customer phone number
   - Adds location pin
   - Sets appointment time
   - Enters service amount
4. Admin assigns to technician in that country
5. Order saved with "Assigned" status
6. Technician will see it during morning access
```

### **Workflow 2: Technician Morning Routine**
```
1. Technician arrives at 5:00 AM
2. Logs into system
3. Views assigned orders for the day
4. Checks location pins and client numbers
5. Plans route for the day
6. Updates orders to "In Progress" as starting each job
7. Marks "Completed" when done
8. Adds completion notes
```

### **Workflow 3: Tracking Complaints**
```
1. Client calls back with complaint
2. Admin finds the order
3. Opens order details
4. Goes to "Success Tracking" section
5. Checks "Has Complaint" checkbox
6. Enters complaint details
7. May assign for repeat service
8. Saves and notifies technician
```

---

## 🚨 **Troubleshooting**

### **Technician Can't Login**
**Problem:** Access restricted message  
**Solution:** Check current time - must be 5 AM - 12 PM

### **Technician Sees No Orders**
**Possible Causes:**
- No orders assigned yet
- Orders assigned to different country
- Wrong technician country setting

**Solution:** Admin should:
1. Check technician's country field
2. Verify orders are assigned to correct technician
3. Ensure country matches order location

### **Order Number Not Generated**
**Solution:** Order numbers auto-generate on save - just save the order

### **Payment Balance Wrong**
**Check:** Amount Paid should not exceed Amount  
**Verify:** Balance = Amount - Amount Paid

---

## 📚 **API Endpoints** (Future)

Currently admin-only web interface. API can be added:
```
GET  /api/orders/           - List orders
POST /api/orders/           - Create order
GET  /api/orders/{id}/      - Order details
PUT  /api/orders/{id}/      - Update order
GET  /api/stats/            - Dashboard statistics
GET  /api/technicians/      - List technicians by country
```

---

## 🔄 **Order States Explained**

| Status | Who Sets | Description |
|--------|----------|-------------|
| **Pending** | Admin | Order created, not assigned |
| **Assigned** | System | Technician assigned to order |
| **In Progress** | Technician | Service being performed |
| **Completed** | Technician | Service finished |
| **Cancelled** | Admin | Order cancelled |

---

## 💡 **Best Practices**

### **For Admins:**
1. ✅ Always add location pin for technician navigation
2. ✅ Assign orders to technicians in correct country
3. ✅ Track complaints immediately when reported
4. ✅ Review successful orders to identify best technicians
5. ✅ Add special instructions for complex jobs

### **For Technicians:**
1. ✅ Check system every morning at 5 AM
2. ✅ Update status as you progress through the day
3. ✅ Add detailed completion notes
4. ✅ Report any issues immediately
5. ✅ Call clients if location pin is unclear

---

## 📖 **System Requirements**

- **Python**: 3.8+
- **Django**: 6.0.3
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **OS**: Windows, Linux, macOS
- **Browser**: Any modern browser for admin interface

---

## 🎓 **Training Guide**

### **New Admin Training:**
1. Log in to system
2. Practice creating test orders
3. Learn to assign technicians
4. Understand success tracking
5. Review dashboard daily

### **New Technician Training:**
1. Learn morning access hours
2. Practice viewing assigned orders
3. Learn to update order status
4. Practice adding completion notes
5. Understand complaint process

---

## 📞 **Support**

For technical support or questions, contact system administrator.

---

**Version:** 2.0.0 (Fumigation Optimized)  
**Last Updated:** March 2026  
**Developed for:** Sanok Fumigation Services  
**Countries:** Kenya 🇰🇪 | Uganda 🇺🇬 | Zambia 🇿🇲 | South Africa 🇿🇦

---

🦟 **Keep homes and businesses pest-free across Africa!** 🌍
