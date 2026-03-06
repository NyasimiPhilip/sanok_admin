# Sanok Admin - Production Deployment Guide

This guide explains how to deploy the Sanok Admin Fumigation Management System on a production server with PostgreSQL.

## Prerequisites

- Ubuntu/Debian server (or any Linux distribution)
- Python 3.10 or higher
- PostgreSQL 12 or higher
- Nginx (web server)
- Domain name (optional but recommended)
- SSH access to your server

## Step 1: Server Setup

### Update system packages
```bash
sudo apt update
sudo apt upgrade -y
```

### Install required system packages
```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

## Step 2: PostgreSQL Database Setup

### Access PostgreSQL
```bash
sudo -u postgres psql
```

### Inside PostgreSQL shell, create database and user
```sql
CREATE DATABASE sanok_admin_db;
CREATE USER sanok_admin WITH PASSWORD 'your-secure-password';
ALTER ROLE sanok_admin SET client_encoding TO 'utf8';
ALTER ROLE sanok_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE sanok_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sanok_admin_db TO sanok_admin;
\q
```

## Step 3: Application Setup

### Create application directory
```bash
sudo mkdir -p /var/www/sanok_admin
sudo chown $USER:$USER /var/www/sanok_admin
cd /var/www/sanok_admin
```

### Clone or upload your code
```bash
# If using git:
git clone <your-repository-url> .

# Or upload files via SCP/SFTP to /var/www/sanok_admin
```

### Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Environment Configuration

### Create .env file
```bash
nano .env
```

### Add the following (adjust values):
```
DJANGO_SECRET_KEY=generate-a-new-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

USE_POSTGRES=True
POSTGRES_DB=sanok_admin_db
POSTGRES_USER=sanok_admin
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Generate a new secret key
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Step 5: Django Setup

### Run migrations
```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### Create super admin
```bash
python manage.py setup_demo --skip-sample-data
# Or create manually:
python manage.py createsuperuser
```

### Collect static files
```bash
python manage.py collectstatic --noinput
```

## Step 6: Gunicorn Setup

### Test Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 sanok_admin.wsgi:application
```

### Create Gunicorn systemd service
```bash
sudo nano /etc/systemd/system/sanok_admin.service
```

### Add the following content:
```ini
[Unit]
Description=Sanok Admin Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sanok_admin
Environment="PATH=/var/www/sanok_admin/venv/bin"
EnvironmentFile=/var/www/sanok_admin/.env
ExecStart=/var/www/sanok_admin/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/sanok_admin/sanok_admin.sock \
    sanok_admin.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Set proper permissions
```bash
sudo chown -R www-data:www-data /var/www/sanok_admin
```

### Start and enable Gunicorn service
```bash
sudo systemctl start sanok_admin
sudo systemctl enable sanok_admin
sudo systemctl status sanok_admin
```

## Step 7: Nginx Configuration

### Create Nginx configuration
```bash
sudo nano /etc/nginx/sites-available/sanok_admin
```

### Add the following:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/sanok_admin/staticfiles/;
    }

    location /media/ {
        alias /var/www/sanok_admin/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sanok_admin/sanok_admin.sock;
    }
}
```

### Enable the site
```bash
sudo ln -s /etc/nginx/sites-available/sanok_admin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: SSL/HTTPS Setup (Recommended)

### Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Obtain SSL certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Auto-renewal is configured automatically

## Step 9: Firewall Configuration

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Step 10: Create Initial Users

### Access your site
Visit: https://yourdomain.com/

### Log in and create users
1. Log in with super admin credentials
2. Navigate to Users section
3. Create admins for each country
4. Create technicians and assign them to countries

## Maintenance Commands

### View logs
```bash
# Gunicorn logs
sudo journalctl -u sanok_admin -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Restart application
```bash
sudo systemctl restart sanok_admin
sudo systemctl restart nginx
```

### Update application
```bash
cd /var/www/sanok_admin
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sanok_admin
```

### Database backup
```bash
pg_dump -U sanok_admin sanok_admin_db > backup_$(date +%Y%m%d).sql
```

### Database restore
```bash
psql -U sanok_admin sanok_admin_db < backup_20260306.sql
```

## Troubleshooting

### Check Gunicorn status
```bash
sudo systemctl status sanok_admin
```

### Check Nginx status
```bash
sudo systemctl status nginx
```

### Check database connection
```bash
source venv/bin/activate
python manage.py dbshell
```

### View error logs
```bash
sudo journalctl -u sanok_admin -n 50
```

### Permission issues
```bash
sudo chown -R www-data:www-data /var/www/sanok_admin
sudo chmod -R 755 /var/www/sanok_admin
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| DJANGO_SECRET_KEY | Django secret key (generate new one) | random-50-char-string |
| DJANGO_DEBUG | Debug mode (False in production) | False |
| DJANGO_ALLOWED_HOSTS | Allowed hostnames (comma-separated) | yourdomain.com,www.yourdomain.com |
| USE_POSTGRES | Use PostgreSQL database | True |
| POSTGRES_DB | Database name | sanok_admin_db |
| POSTGRES_USER | Database user | sanok_admin |
| POSTGRES_PASSWORD | Database password | secure-password |
| POSTGRES_HOST | Database host | localhost |
| POSTGRES_PORT | Database port | 5432 |

## Security Checklist

- [ ] Changed DJANGO_SECRET_KEY to a new random value
- [ ] Set DJANGO_DEBUG=False in production
- [ ] Configured ALLOWED_HOSTS properly
- [ ] Used strong PostgreSQL password
- [ ] Configured SSL/HTTPS with Certbot
- [ ] Enabled firewall (UFW)
- [ ] Set proper file permissions (www-data)
- [ ] Regular database backups scheduled
- [ ] Keep system packages updated
- [ ] Monitor application logs

## Support

For issues or questions, refer to:
- Django documentation: https://docs.djangoproject.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/
- Nginx documentation: https://nginx.org/en/docs/

## Time Zone Configuration

The application enforces technician access between 5 AM - 12 PM. Make sure to set the correct timezone:

1. Edit settings.py: `TIME_ZONE = 'Africa/Nairobi'` (or appropriate timezone)
2. Run migrations again if changed
3. Restart the application

Available timezones:
- Kenya: Africa/Nairobi
- Uganda: Africa/Kampala
- Zambia: Africa/Lusaka
- South Africa: Africa/Johannesburg
