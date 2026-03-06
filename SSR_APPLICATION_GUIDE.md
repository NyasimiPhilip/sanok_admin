# Sanok Fumigation SSR Application Guide

## 🌟 Overview
Complete Server-Side Rendered (SSR) Django application for fumigation order management with role-based access control.

## 📁 Template Structure

### Base Templates
- **base.html** - Main template with navigation, styling, and layout
- **login.html** - Authentication page with custom styling
- **home.html** - Landing page showcasing services

### Dashboard Templates
- **dashboard.html** - Unified dashboard adapting to user role (Super Admin, Admin, Technician)
  - Statistics cards with order counts
  - Revenue tracking
  - Country-based order breakdown
  - Recent orders list
  - Today's schedule for technicians

### Booking/Order Management Templates
- **booking_list.html** - Paginated order list with advanced filtering
  - Filter by status, country, pest type, complaints
  - Search by order number, phone, location
  - Visual indicators for complaints
- **booking_detail.html** - Comprehensive order details
  - Order information with status badges
  - Location and contact details
  - Technician assignment
  - Complaint tracking
  - Action buttons (edit, delete, status updates)
- **booking_form.html** - Create/edit order form
  - Date/time scheduling
  - Country and location selection
  - Pest type dropdown
  - Technician assignment
  - Dynamic complaint details field

### User Management Templates
- **user_list.html** - User directory with filtering
  - Role-based filtering (Super Admin, Admin, Technician)
  - Country filtering
  - Active/inactive status
  - Search functionality
  - User statistics
- **user_detail.html** - User profile and statistics
  - Profile information
  - Work statistics for technicians
  - Access permissions display
  - Recent orders (for technicians)
- **user_form.html** - Create/edit user form
  - Role selection with permission preview
  - Password validation for new users
  - Dynamic country field for technicians
  - Active status toggle

## 🎨 Styling Features
- Gradient backgrounds and modern cards
- Responsive grid layouts
- Color-coded status badges
- Flag emojis for countries
- Icon integration
- Hover effects and transitions
- Mobile-friendly design

## 🔐 User Roles & Access

### Super Admin (🔑)
- **Access**: 24/7
- **Permissions**:
  - Create/delete admins and technicians
  - Manage all orders across all countries
  - View all statistics and reports
  - Full system access

### Admin (👨‍💼)
- **Access**: 24/7
- **Permissions**:
  - Create/delete technicians
  - Create orders in any country
  - Assign technicians to orders
  - View all orders and statistics
  - Cannot manage other admins

### Technician (🔧)
- **Access**: 5:00 AM - 12:00 PM only
- **Permissions**:
  - View assigned orders only
  - Update order status
  - View own profile
  - Cannot create orders or manage users

## 🚀 URL Structure

### Authentication
- `/` - Login page
- `/login/` - Login page
- `/logout/` - Logout and redirect to login
- `/home/` - Landing page (requires login)

### Dashboard
- `/dashboard/` - Role-specific dashboard

### Orders (Bookings)
- `/bookings/` - List all orders (paginated, with filters)
- `/bookings/create/` - Create new order (Admin/Super Admin only)
- `/bookings/<id>/` - View order details
- `/bookings/<id>/edit/` - Edit order (Admin/Super Admin only)
- `/bookings/<id>/delete/` - Delete order (Admin/Super Admin only)
- `/bookings/<id>/status/` - Update order status
- `/bookings/<id>/complaint/` - Toggle complaint status

### Users
- `/users/` - List all users (paginated, with filters)
- `/users/create/` - Create new user (Admin/Super Admin only)
- `/users/<id>/` - View user profile
- `/users/<id>/edit/` - Edit user (Admin/Super Admin only)
- `/users/<id>/delete/` - Delete user (Admin/Super Admin only)
- `/users/<id>/toggle-active/` - Activate/deactivate user

### Admin Panel
- `/admin/` - Django admin interface (for advanced management)

## 📝 Views Overview

### Authentication Views
- `login_view()` - Handles login with time validation for technicians
- `logout_view()` - Handles logout
- `home_view()` - Displays landing page

### Dashboard Views
- `dashboard_view()` - Shows role-specific dashboard with statistics

### Booking Views
- `booking_list_view()` - Paginated list with filtering
- `booking_detail_view()` - Single order details
- `booking_create_view()` - Create new order
- `booking_edit_view()` - Edit existing order
- `booking_delete_view()` - Delete order
- `booking_status_update_view()` - Update status
- `booking_complaint_toggle_view()` - Toggle complaint status

### User Management Views
- `user_list_view()` - Paginated user list with filtering
- `user_detail_view()` - User profile with statistics
- `user_create_view()` - Create new user with permission checks
- `user_edit_view()` - Edit user profile
- `user_delete_view()` - Delete user
- `user_toggle_active_view()` - Activate/deactivate user

## 🔥 Key Features

### Filtering & Search
- **Orders**: Filter by status, country, pest type, complaints; Search by order #, phone, location
- **Users**: Filter by role, country, active status; Search by name, username, email

### Pagination
- Both orders and users lists support pagination (20 items per page)
- Page navigation with First/Previous/Next/Last links

### Complaint Tracking
- Visual indicators (✅/⚠️) for complaint status
- Dedicated complaint details field
- Quick toggle complaint status

### Permission-Based UI
- Templates adapt based on user role
- Action buttons only shown when permitted
- Automatic filtering of visible data

### Responsive Design
- Mobile-friendly layouts
- Flexible grid systems
- Touch-friendly controls

## 🛠️ Setup Instructions

1. **Ensure migrations are created and applied**:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create demo data**:
   ```powershell
   python manage.py setup_demo --create-sample-data
   ```

3. **Run development server**:
   ```powershell
   python manage.py runserver
   ```

4. **Access the application**:
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🔑 Demo Credentials

### Super Admin
- Username: `superadmin`
- Password: `super123`

### Admin
- Username: `admin`
- Password: `admin123`

### Technicians
All technicians use password: `tech123`
- Kenya: `kenya_tech1`, `kenya_tech2`
- Uganda: `uganda_tech1`
- Zambia: `zambia_tech1`
- South Africa: `sa_tech1`

## 🌍 Supported Countries
- 🇰🇪 Kenya
- 🇺🇬 Uganda
- 🇿🇲 Zambia
- 🇿🇦 South Africa

## 🐛 Pest Types Covered
1. 🐀 Rodents
2. 🪳 Cockroaches
3. 🐜 Termites
4. 🛏️ Bed Bugs
5. 🐜 Ants
6. 🦟 Mosquitoes
7. 🪰 Flies
8. Other

## 📊 Order Status Flow
1. **Pending** → Initial state when order is created
2. **Assigned** → Technician has been assigned
3. **In Progress** → Technician is working on it
4. **Completed** → Service finished
5. **Cancelled** → Order cancelled

## ⏰ Time Restrictions
- **Technicians**: Can only access the system between 5:00 AM - 12:00 PM
- **Admins & Super Admins**: 24/7 access
- Time check happens at login and via middleware

## 💡 Tips for Usage

### For Admins
1. Use the dashboard to monitor overall system statistics
2. Create orders through the "New Order" button
3. Assign technicians based on country for efficiency
4. Track complaints to monitor service quality

### For Technicians
1. Check "Today's Schedule" on dashboard each morning
2. Update order status as you progress
3. Access is limited to morning hours - plan accordingly
4. View only your assigned orders

### For Super Admins
1. Use user management to create admins and technicians
2. Monitor system-wide statistics
3. Ensure proper country distribution of technicians
4. Access Django admin panel for advanced configuration

## 🔒 Security Features
- Login required for all pages except login page
- Role-based access control throughout
- Time-based access restrictions for technicians
- Password validation on user creation
- CSRF protection on all forms
- Permission checks on all actions

## 📱 Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design works on mobile, tablet, and desktop
- No external CSS frameworks required - all custom styling

## 🎯 Next Steps
1. Test the complete workflow from login to order completion
2. Customize colors/styling in base.html if needed
3. Add more pest types in models.py if required
4. Configure email notifications (future enhancement)
5. Add export functionality for reports (future enhancement)

## 📞 Support
For issues or questions, check the Django admin panel logs or console output.
