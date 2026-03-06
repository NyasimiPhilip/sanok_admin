# Production Setup Quick Reference

## What's Been Configured

Your Sanok Admin application is now configured for production PostgreSQL deployment. Here's what was changed:

### 1. Database Configuration
- **Changed from**: SQLite (local development only)
- **Changed to**: PostgreSQL with environment variable support
- **Fallback**: Can still use SQLite locally by setting `USE_POSTGRES=False`

### 2. Environment Variables
All sensitive configuration now uses environment variables:
- `DJANGO_SECRET_KEY` - Secret key (generate new one for production)
- `DJANGO_DEBUG` - Debug mode (False in production)
- `DJANGO_ALLOWED_HOSTS` - Comma-separated list of allowed domains
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Database host (usually localhost)
- `POSTGRES_PORT` - Database port (usually 5432)
- `DJANGO_TIMEZONE` - Timezone for the server (default: Africa/Nairobi)

### 3. Security Settings
Added production security settings (auto-enabled when DEBUG=False):
- SSL redirect
- Secure cookies
- HSTS headers
- XSS protection
- Content type nosniff

### 4. Static & Media Files
- `STATIC_ROOT` - Configured for collectstatic command
- `MEDIA_ROOT` - Configured for file uploads

### 5. Dependencies Added
- `psycopg2-binary` - PostgreSQL adapter
- `gunicorn` - Production WSGI server
- `python-decouple` - Environment variable management (optional)
- `pytz` - Timezone support

## Quick Start: Local Testing with PostgreSQL

1. **Install PostgreSQL dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env file** (copy from .env.example):
   ```bash
   cp .env.example .env
   ```

3. **Edit .env** with your local PostgreSQL settings:
   ```
   USE_POSTGRES=True
   POSTGRES_DB=sanok_admin_db
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create super admin**:
   ```bash
   python manage.py setup_demo
   ```

6. **Test the application**:
   ```bash
   python manage.py runserver
   ```

## Quick Start: Local Testing with SQLite (No PostgreSQL)

If you don't have PostgreSQL installed locally, you can still test with SQLite:

1. **Create .env file**:
   ```
   USE_POSTGRES=False
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create super admin**:
   ```bash
   python manage.py setup_demo
   ```

4. **Test the application**:
   ```bash
   python manage.py runserver
   ```

## Production Deployment

Follow the complete **DEPLOYMENT_GUIDE.md** for step-by-step server setup instructions.

### Key Steps:
1. Set up Ubuntu/Debian server
2. Install PostgreSQL and create database
3. Upload code to `/var/www/sanok_admin`
4. Create `.env` file with production settings
5. Run migrations and collect static files
6. Configure Gunicorn systemd service
7. Configure Nginx reverse proxy
8. Set up SSL with Certbot
9. Configure firewall

## Environment Variables (.env file)

Create a `.env` file in the project root with these variables:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,server-ip
DJANGO_TIMEZONE=Africa/Nairobi

# Database (PostgreSQL)
USE_POSTGRES=True
POSTGRES_DB=sanok_admin_db
POSTGRES_USER=sanok_admin
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Timezone Options

Set `DJANGO_TIMEZONE` based on your primary operating location:
- **Kenya**: `Africa/Nairobi` (default)
- **Uganda**: `Africa/Kampala`
- **Zambia**: `Africa/Lusaka`
- **South Africa**: `Africa/Johannesburg`

This is important for the technician access time restrictions (5 AM - 12 PM).

## Testing Database Connection

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Test database connection
python manage.py dbshell
```

## Common Commands

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create super admin
python manage.py setup_demo

# Collect static files (production)
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver

# Run production server (Gunicorn)
gunicorn sanok_admin.wsgi:application --bind 0.0.0.0:8000
```

## Files Created/Modified

1. **sanok_admin/settings.py** - Updated with PostgreSQL config and environment variables
2. **requirements.txt** - Added psycopg2-binary, gunicorn, python-decouple, pytz
3. **.env.example** - Template for environment variables
4. **.gitignore** - Protect sensitive files from git
5. **DEPLOYMENT_GUIDE.md** - Complete production deployment instructions
6. **PRODUCTION_SETUP.md** - This file (quick reference)

## Security Checklist

Before deploying to production:
- [ ] Generate new `DJANGO_SECRET_KEY` (never use the default)
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Update `DJANGO_ALLOWED_HOSTS` with your domain
- [ ] Use strong PostgreSQL password
- [ ] Set up SSL/HTTPS
- [ ] Configure firewall
- [ ] Regular database backups
- [ ] Keep dependencies updated

## Need Help?

- **Full deployment guide**: See DEPLOYMENT_GUIDE.md
- **Application usage**: See SSR_APPLICATION_GUIDE.md
- **Quick start**: See QUICK_START.md

## Support Contact

For technical issues:
1. Check application logs: `sudo journalctl -u sanok_admin -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify database connection: `python manage.py dbshell`
