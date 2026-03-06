from django.core.management.base import BaseCommand
from django.utils import timezone
from bookings.models import CustomUser, Booking, BookingCommand
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Set up initial demo data for the fumigation order system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--super-admin-username',
            type=str,
            default='superadmin',
            help='Username for super admin account'
        )
        parser.add_argument(
            '--super-admin-password',
            type=str,
            default='super123',
            help='Password for super admin account'
        )
        parser.add_argument(
            '--admin-username',
            type=str,
            default='admin',
            help='Username for admin account'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='admin123',
            help='Password for admin account'
        )
        parser.add_argument(
            '--create-sample-data',
            action='store_true',
            help='Create sample fumigation orders'
        )

    def handle(self, *args, **options):
        super_admin_username = options['super_admin_username']
        super_admin_password = options['super_admin_password']
        admin_username = options['admin_username']
        admin_password = options['admin_password']
        create_samples = options['create_sample_data']

        self.stdout.write(self.style.SUCCESS('🚀 Setting up Sanok Fumigation Order System...'))
        self.stdout.write('')

        # Create super admin user
        if not CustomUser.objects.filter(username=super_admin_username).exists():
            super_admin = CustomUser.objects.create_superuser(
                username=super_admin_username,
                email=f'{super_admin_username}@sanok.com',
                password=super_admin_password,
                role='super_admin',
                first_name='Super',
                last_name='Admin'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Super Admin user created: {super_admin_username}'))
            self.stdout.write(f'   Password: {super_admin_password}')
        else:
            super_admin = CustomUser.objects.get(username=super_admin_username)
            super_admin.role = 'super_admin'
            super_admin.is_staff = True
            super_admin.is_superuser = True
            super_admin.save()
            self.stdout.write(self.style.WARNING(f'⚠️  Super Admin user already exists: {super_admin_username}'))

        # Create admin user
        if not CustomUser.objects.filter(username=admin_username).exists():
            admin = CustomUser.objects.create_user(
                username=admin_username,
                email=f'{admin_username}@sanok.com',
                password=admin_password,
                role='admin',
                is_staff=True,
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Admin user created: {admin_username}'))
            self.stdout.write(f'   Password: {admin_password}')
        else:
            admin = CustomUser.objects.get(username=admin_username)
            admin.role = 'admin'
            admin.is_staff = True
            admin.save()
            self.stdout.write(self.style.WARNING(f'⚠️  Admin user already exists: {admin_username}'))

        # Create sample technicians for each country
        technicians = []
        tech_data = [
            ('kenya_tech1', 'James', 'Mwangi', 'kenya', '+254-700-123456'),
            ('kenya_tech2', 'Sarah', 'Wanjiku', 'kenya', '+254-700-123457'),
            ('uganda_tech1', 'Moses', 'Okello', 'uganda', '+256-700-123456'),
            ('zambia_tech1', 'Patrick', 'Banda', 'zambia', '+260-97-1234567'),
            ('sa_tech1', 'Sipho', 'Ndlovu', 'south_africa', '+27-82-1234567'),
        ]

        for username, first, last, country, phone in tech_data:
            if not CustomUser.objects.filter(username=username).exists():
                tech = CustomUser.objects.create_user(
                    username=username,
                    email=f'{username}@sanok.com',
                    password='tech123',
                    role='technician',
                    is_staff=True,
                    first_name=first,
                    last_name=last,
                    country=country,
                    phone_number=phone
                )
                technicians.append(tech)
                self.stdout.write(self.style.SUCCESS(
                    f'✅ Technician created: {username} ({country.replace("_", " ").title()}) - password: tech123'
                ))
            else:
                tech = CustomUser.objects.get(username=username)
                tech.role = 'technician'
                tech.is_staff = True
                tech.country = country
                tech.phone_number = phone
                tech.save()
                technicians.append(tech)
                self.stdout.write(self.style.WARNING(f'⚠️  Technician already exists: {username}'))

        if create_samples and technicians:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('📋 Creating sample fumigation orders...'))

            countries = ['kenya', 'uganda', 'zambia', 'south_africa']
            locations = [
                ('Nairobi CBD, Kenyatta Avenue', '🇰🇪 Kenya'),
                ('Kampala, Nakasero', '🇺🇬 Uganda'),
                ('Lusaka, Cairo Road', '🇿🇲 Zambia'),
                ('Johannesburg, Sandton', '🇿🇦 South Africa'),
                ('Mombasa, Diani Beach Resort', '🇰🇪 Kenya'),
                ('Entebbe, Airport Road', '🇺🇬 Uganda'),
                ('Kitwe, Central Business District', '🇿🇲 Zambia'),
                ('Cape Town, Waterfront', '🇿🇦 South Africa'),
            ]
            
            clients = [
                ('John Mwangi', '+254-722-345678'),
                ('Alice Namukasa', '+256-772-123456'),
                ('Peter Banda', '+260-97-5551234'),
                ('Sarah Nkomo', '+27-83-4567890'),
                ('David Kariuki', '+254-733-654321'),
                ('Grace Akello', '+256-701-987654'),
                ('Joseph Chilufya', '+260-96-7771234'),
                ('Thabo Dlamini', '+27-81-2223333'),
            ]

            pest_types = ['rodents', 'cockroaches', 'termites', 'bed_bugs', 'ants', 'mosquitoes', 'flies', 'other']
            statuses = ['pending', 'assigned', 'in_progress', 'completed']
            
            for i in range(8):
                country = countries[i % 4]
                location, _ = locations[i]
                client_name, client_phone = clients[i]
                
                # Get technician for this country
                tech = [t for t in technicians if t.country == country][0]
                
                status = random.choice(statuses)
                pest_type = random.choice(pest_types)
                
                # Create order
                booking = Booking.objects.create(
                    order_time=timezone.now() + timedelta(days=i, hours=random.randint(8, 16)),
                    country=country,
                    location_pin=f'https://maps.google.com/?q={location}',
                    location_address=location,
                    client_phone=client_phone,
                    pest_type=pest_type,
                    amount=round(random.uniform(2000, 8000), 2),
                    status=status,
                    assigned_technician=tech if status != 'pending' else None,
                    assigned_at=timezone.now() - timedelta(hours=random.randint(1, 48)) if status != 'pending' else None,
                    created_by=admin,
                    notes=f'{pest_type.replace("_", " ").title()} fumigation service requested'
                )
                
                # Add complaint tracking for completed orders
                if status == 'completed':
                    booking.completed_at = timezone.now() - timedelta(hours=random.randint(1, 24))
                    
                    # 75% no complaint, 25% with complaint
                    if random.random() < 0.25:
                        booking.has_complaint = True
                        booking.complaint_details = random.choice([
                            'Client reported seeing pests after 2 days',
                            'Pests returned within a week',
                            'Strong chemical smell remained too long',
                            'Client not satisfied with coverage'
                        ])
                    else:
                        booking.has_complaint = False
                
                booking.save()

                # Add some instructions to orders
                if random.random() > 0.5:
                    BookingCommand.objects.create(
                        booking=booking,
                        instruction_type=random.choice(['equipment', 'access', 'safety', 'client_request']),
                        description=random.choice([
                            'Bring extra fumigation equipment for large area',
                            'Call client 30 minutes before arrival',
                            'Property has pets - ensure safe chemicals used',
                            'Client requests organic/eco-friendly treatment',
                            'Access code: 1234#. Gate code: 5678',
                            'Wear full protective gear - commercial kitchen',
                        ]),
                        created_by=admin
                    )

                country_flag = {'kenya': '🇰🇪', 'uganda': '🇺🇬', 'zambia': '🇿🇲', 'south_africa': '🇿🇦'}
                self.stdout.write(
                    f'   📝 Order {booking.order_number}: {country_flag[country]} {client_name} - {status}'
                )

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'✅ Created 8 sample fumigation orders'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('🎉 Setup Complete!'))
        self.stdout.write('')
        self.stdout.write('📌 Login Credentials:')
        self.stdout.write(f'   Super Admin: {super_admin_username} / {super_admin_password}')
        self.stdout.write(f'   Admin: {admin_username} / {admin_password}')
        self.stdout.write('')
        self.stdout.write('   Technicians (password for all: tech123):')
        self.stdout.write('   🇰🇪 Kenya: kenya_tech1, kenya_tech2')
        self.stdout.write('   🇺🇬 Uganda: uganda_tech1')
        self.stdout.write('   🇿🇲 Zambia: zambia_tech1')
        self.stdout.write('   🇿🇦 South Africa: sa_tech1')
        self.stdout.write('')
        self.stdout.write('🌐 Access the admin panel at: http://127.0.0.1:8000/admin/')
        self.stdout.write('')
        self.stdout.write('👤 User Hierarchy:')
        self.stdout.write('   Super Admin: Can create/delete admins and technicians')
        self.stdout.write('   Admin: Can create/delete technicians, input orders 24/7')
        self.stdout.write('   Technician: View assigned orders only')
        self.stdout.write('')
        self.stdout.write('⏰ Access Hours:')
        self.stdout.write('   Technicians: 5:00 AM - 12:00 PM (Morning only)')
        self.stdout.write('   Admin & Super Admin: 24/7')
        self.stdout.write('')
        self.stdout.write('🗺️  Countries: Kenya, Uganda, Zambia, South Africa')
        self.stdout.write('🐛 Pest Types: Rodents, Cockroaches, Termites, Bed Bugs, Ants, Mosquitoes, Flies, Other')
        self.stdout.write(self.style.SUCCESS('=' * 70))
