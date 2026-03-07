#!/usr/bin/env bash
# reset_users.sh
# Clears ALL users in the database and creates the Festus Kinyua super admin.
# Usage:  bash reset_users.sh
#
# Run from the project root where manage.py lives.
# Make executable first:  chmod +x reset_users.sh

set -e  # exit immediately on any error

PYTHON="${PYTHON:-python}"   # override with: PYTHON=python3 bash reset_users.sh

echo "============================================"
echo " Sanok Fumigation — Reset & Seed Users"
echo "============================================"

# ── 1. Activate virtual environment if present ──────────────────────────────
if [ -f "venv/bin/activate" ]; then
    echo "[INFO] Activating venv (venv/bin/activate)"
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    echo "[INFO] Activating venv (.venv/bin/activate)"
    source .venv/bin/activate
else
    echo "[INFO] No venv found — using system Python"
fi

# ── 2. Delete all users ──────────────────────────────────────────────────────
echo ""
echo "[STEP 1] Deleting all existing users..."
$PYTHON manage.py shell << 'PYEOF'
from bookings.models import CustomUser
count, _ = CustomUser.objects.all().delete()
print(f"  Deleted {count} user record(s).")
PYEOF

# ── 3. Create Festus Kinyua super admin ──────────────────────────────────────
echo ""
echo "[STEP 2] Creating Super Admin — Festus Kinyua..."
$PYTHON manage.py shell << 'PYEOF'
from bookings.models import CustomUser

username = 'Kinyua2026'
password = 'Kinyua2026'

if CustomUser.objects.filter(username=username).exists():
    print(f"  User '{username}' already exists — skipping creation.")
else:
    user = CustomUser.objects.create_user(
        username=username,
        password=password,
        first_name='Festus',
        last_name='Kinyua',
        role='super_admin',
        is_staff=True,
        is_superuser=True,
    )
    print(f"  Created: {user.get_full_name()} (username={user.username}, role={user.role})")
PYEOF

# ── 4. Done ──────────────────────────────────────────────────────────────────
echo ""
echo "============================================"
echo " Done. Login with:"
echo "   Username : Kinyua2026"
echo "   Password : Kinyua2026"
echo "============================================"
