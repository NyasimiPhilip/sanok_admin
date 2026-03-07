#!/bin/bash
# Production Setup Script for sanok.lat
# Run this on your server as root

set -e

echo "🚀 Setting up Sanok Admin Production Server..."

# 1. Update .env file
echo "📝 Updating .env file..."
cat > .env << 'EOF'
# Django Settings
DJANGO_SECRET_KEY=django-insecure-8k#m2v$x9p@7w!q5nz&4f^ht*6r+jy3u-8e=a1s%d9g0c2b
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,78.111.67.161,sanok.lat,www.sanok.lat
DJANGO_TIMEZONE=Africa/Nairobi

# Database Configuration (PostgreSQL)
USE_POSTGRES=True
POSTGRES_DB=sanok_admin_db
POSTGRES_USER=sanok_admin
POSTGRES_PASSWORD=SanokAdmin2026!Secure#Pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EOF

# 2. Collect static files
echo "📦 Collecting static files..."
source venv/bin/activate
python manage.py collectstatic --noinput

# 3. Set proper permissions
echo "🔒 Setting permissions..."
chmod -R 755 /root/sanok_admin

# 4. Create Gunicorn systemd service
echo "⚙️  Creating Gunicorn service..."
cat > /etc/systemd/system/sanok_admin.service << 'EOF'
[Unit]
Description=Sanok Admin Gunicorn daemon
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/sanok_admin
Environment="PATH=/root/sanok_admin/venv/bin"
EnvironmentFile=/root/sanok_admin/.env
ExecStart=/root/sanok_admin/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/root/sanok_admin/sanok_admin.sock \
    sanok_admin.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 5. Start and enable Gunicorn
echo "🔄 Starting Gunicorn service..."
systemctl daemon-reload
systemctl start sanok_admin
systemctl enable sanok_admin
systemctl status sanok_admin --no-pager

# 6. Install and configure Nginx
echo "🌐 Installing Nginx..."
apt install -y nginx

# 7. Create Nginx configuration
echo "⚙️  Configuring Nginx..."
cat > /etc/nginx/sites-available/sanok_admin << 'EOF'
server {
    listen 80;
    server_name sanok.lat www.sanok.lat 78.111.67.161;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /root/sanok_admin/staticfiles/;
    }

    location /media/ {
        alias /root/sanok_admin/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/sanok_admin/sanok_admin.sock;
    }
}
EOF

# 8. Enable Nginx site
echo "✅ Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/sanok_admin /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 9. Configure firewall
echo "🔥 Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

# 10. Install Certbot for SSL
echo "🔐 Installing Certbot for SSL..."
apt install -y certbot python3-certbot-nginx

echo ""
echo "✅ Production setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Make sure your domain sanok.lat points to 78.111.67.161"
echo "2. Run: certbot --nginx -d sanok.lat -d www.sanok.lat"
echo "3. Visit: https://sanok.lat"
echo ""
echo "🔍 Check status:"
echo "  - Gunicorn: systemctl status sanok_admin"
echo "  - Nginx: systemctl status nginx"
echo "  - Logs: journalctl -u sanok_admin -f"
echo ""
