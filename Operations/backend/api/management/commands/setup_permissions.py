from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.db import models
from api.models import Permission, Role, UserProfile


class Command(BaseCommand):
    help = 'Set up required permissions and admin role for the application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-existing-admins',
            action='store_true',
            help='Also fix existing admin users by assigning the Admin role',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up permissions and admin role...'))

        with transaction.atomic():
            # Create all required permissions
            permissions_created = self.create_permissions()

            # Create or update Admin role with all permissions
            admin_role = self.create_admin_role()

            # Fix existing admin users if requested
            if options['fix_existing_admins']:
                self.fix_existing_admin_users(admin_role)

        self.stdout.write(self.style.SUCCESS(f'✅ Setup complete! Created {permissions_created} permissions'))

    def create_permissions(self):
        """Create all required permissions for the application"""
        self.stdout.write('Creating permissions...')

        # Define all the model permissions needed based on ViewSet permission classes
        model_permissions = [
            # Patient permissions (required by PatientViewSet)
            ('patient_read', 'Can read patient data'),
            ('patient_write', 'Can create patient records'),
            ('patient_modify', 'Can modify patient records'),
            ('patient_delete', 'Can delete patient records'),

            # Trip permissions (required by TripViewSet)
            ('trip_read', 'Can read trip data'),
            ('trip_write', 'Can create trip records'),
            ('trip_modify', 'Can modify trip records'),
            ('trip_delete', 'Can delete trip records'),

            # Quote permissions (required by QuoteViewSet)
            ('quote_read', 'Can read quote data'),
            ('quote_write', 'Can create quote records'),
            ('quote_modify', 'Can modify quote records'),
            ('quote_delete', 'Can delete quote records'),

            # Passenger permissions (required by PassengerViewSet)
            ('passenger_read', 'Can read passenger data'),
            ('passenger_write', 'Can create passenger records'),
            ('passenger_modify', 'Can modify passenger records'),
            ('passenger_delete', 'Can delete passenger records'),

            # Transaction permissions (required by TransactionViewSet)
            ('transaction_read', 'Can read transaction data'),
            ('transaction_write', 'Can create transaction records'),
            ('transaction_modify', 'Can modify transaction records'),
            ('transaction_delete', 'Can delete transaction records'),

            # TripLine permissions (required by TripLineViewSet)
            ('tripline_read', 'Can read trip line data'),
            ('tripline_write', 'Can create trip line records'),
            ('tripline_modify', 'Can modify trip line records'),
            ('tripline_delete', 'Can delete trip line records'),

            # Contact permissions (for patient/customer data)
            ('contact_read', 'Can read contact data'),
            ('contact_write', 'Can create contact records'),
            ('contact_modify', 'Can modify contact records'),
            ('contact_delete', 'Can delete contact records'),

            # Aircraft permissions (for trip aircraft data)
            ('aircraft_read', 'Can read aircraft data'),
            ('aircraft_write', 'Can create aircraft records'),
            ('aircraft_modify', 'Can modify aircraft records'),
            ('aircraft_delete', 'Can delete aircraft records'),

            # Agreement permissions
            ('agreement_read', 'Can read agreement data'),
            ('agreement_write', 'Can create agreement records'),
            ('agreement_modify', 'Can modify agreement records'),
            ('agreement_delete', 'Can delete agreement records'),

            # CrewLine permissions
            ('crewline_read', 'Can read crew line data'),
            ('crewline_write', 'Can create crew line records'),
            ('crewline_modify', 'Can modify crew line records'),
            ('crewline_delete', 'Can delete crew line records'),

            # Document permissions
            ('document_read', 'Can read document data'),
            ('document_write', 'Can create document records'),
            ('document_modify', 'Can modify document records'),
            ('document_delete', 'Can delete document records'),

            # FBO permissions
            ('fbo_read', 'Can read FBO data'),
            ('fbo_write', 'Can create FBO records'),
            ('fbo_modify', 'Can modify FBO records'),
            ('fbo_delete', 'Can delete FBO records'),

            # Ground permissions
            ('ground_read', 'Can read ground transportation data'),
            ('ground_write', 'Can create ground transportation records'),
            ('ground_modify', 'Can modify ground transportation records'),
            ('ground_delete', 'Can delete ground transportation records'),

            # Airport permissions
            ('airport_read', 'Can read airport data'),
            ('airport_write', 'Can create airport records'),
            ('airport_modify', 'Can modify airport records'),
            ('airport_delete', 'Can delete airport records'),

            # Staff permissions
            ('staff_read', 'Can read staff data'),
            ('staff_write', 'Can create staff records'),
            ('staff_modify', 'Can modify staff records'),
            ('staff_delete', 'Can delete staff records'),

            # Comment permissions
            ('comment_read', 'Can read comment data'),
            ('comment_write', 'Can create comment records'),
            ('comment_modify', 'Can modify comment records'),
            ('comment_delete', 'Can delete comment records'),

            # Modification permissions (for audit trail)
            ('modification_read', 'Can read modification history'),

            # Object-level permissions (required by has_object_permission method)
            # Patient object permissions
            ('patient_read_any', 'Can read any patient record'),
            ('patient_read_own', 'Can read own patient records'),
            ('patient_write_any', 'Can create any patient record'),
            ('patient_write_own', 'Can create own patient records'),
            ('patient_modify_any', 'Can modify any patient record'),
            ('patient_modify_own', 'Can modify own patient records'),
            ('patient_delete_any', 'Can delete any patient record'),
            ('patient_delete_own', 'Can delete own patient records'),

            # Trip object permissions
            ('trip_read_any', 'Can read any trip record'),
            ('trip_read_own', 'Can read own trip records'),
            ('trip_write_any', 'Can create any trip record'),
            ('trip_write_own', 'Can create own trip records'),
            ('trip_modify_any', 'Can modify any trip record'),
            ('trip_modify_own', 'Can modify own trip records'),
            ('trip_delete_any', 'Can delete any trip record'),
            ('trip_delete_own', 'Can delete own trip records'),

            # Quote object permissions
            ('quote_read_any', 'Can read any quote record'),
            ('quote_read_own', 'Can read own quote records'),
            ('quote_write_any', 'Can create any quote record'),
            ('quote_write_own', 'Can create own quote records'),
            ('quote_modify_any', 'Can modify any quote record'),
            ('quote_modify_own', 'Can modify own quote records'),
            ('quote_delete_any', 'Can delete any quote record'),
            ('quote_delete_own', 'Can delete own quote records'),

            # Passenger object permissions
            ('passenger_read_any', 'Can read any passenger record'),
            ('passenger_read_own', 'Can read own passenger records'),
            ('passenger_write_any', 'Can create any passenger record'),
            ('passenger_write_own', 'Can create own passenger records'),
            ('passenger_modify_any', 'Can modify any passenger record'),
            ('passenger_modify_own', 'Can modify own passenger records'),
            ('passenger_delete_any', 'Can delete any passenger record'),
            ('passenger_delete_own', 'Can delete own passenger records'),

            # Transaction object permissions
            ('transaction_read_any', 'Can read any transaction record'),
            ('transaction_read_own', 'Can read own transaction records'),
            ('transaction_write_any', 'Can create any transaction record'),
            ('transaction_write_own', 'Can create own transaction records'),
            ('transaction_modify_any', 'Can modify any transaction record'),
            ('transaction_modify_own', 'Can modify own transaction records'),
            ('transaction_delete_any', 'Can delete any transaction record'),
            ('transaction_delete_own', 'Can delete own transaction records'),

            # TripLine object permissions
            ('tripline_read_any', 'Can read any trip line record'),
            ('tripline_read_own', 'Can read own trip line records'),
            ('tripline_write_any', 'Can create any trip line record'),
            ('tripline_write_own', 'Can create own trip line records'),
            ('tripline_modify_any', 'Can modify any trip line record'),
            ('tripline_modify_own', 'Can modify own trip line records'),
            ('tripline_delete_any', 'Can delete any trip line record'),
            ('tripline_delete_own', 'Can delete own trip line records'),

            # Global permissions (checked by HasModelPermission base class)
            ('any_read', 'Can read any data (global read permission)'),
            ('any_write', 'Can create any records (global write permission)'),
            ('any_modify', 'Can modify any records (global modify permission)'),
            ('any_delete', 'Can delete any records (global delete permission)'),
        ]

        created_count = 0
        for permission_name, description in model_permissions:
            permission, created = Permission.objects.get_or_create(
                name=permission_name,
                defaults={'description': description}
            )
            if created:
                created_count += 1
                self.stdout.write(f'  ✅ Created permission: {permission_name}')
            else:
                self.stdout.write(f'  ✅ Permission already exists: {permission_name}')

        return created_count

    def create_admin_role(self):
        """Create or update the Admin role with all permissions"""
        self.stdout.write('Creating/updating Admin role...')

        # Get or create the Admin role
        admin_role, created = Role.objects.get_or_create(
            name='Admin',
            defaults={'description': 'Full system administrator with all permissions'}
        )

        if created:
            self.stdout.write('  ✅ Created Admin role')
        else:
            self.stdout.write('  ✅ Admin role already exists, updating permissions...')

        # Get all permissions
        all_permissions = Permission.objects.all()

        # Assign all permissions to the Admin role
        admin_role.permissions.set(all_permissions)

        self.stdout.write(f'  ✅ Assigned {all_permissions.count()} permissions to Admin role')

        return admin_role

    def fix_existing_admin_users(self, admin_role):
        """Assign Admin role to existing admin users who don't have it"""
        self.stdout.write('Fixing existing admin users...')

        # Find all superusers and staff users
        admin_users = User.objects.filter(models.Q(is_superuser=True) | models.Q(is_staff=True))

        fixed_count = 0
        for user in admin_users:
            try:
                profile = UserProfile.objects.get(user=user)

                # Check if user already has Admin role
                if not profile.roles.filter(name='Admin').exists():
                    profile.roles.add(admin_role)
                    fixed_count += 1
                    self.stdout.write(f'  ✅ Added Admin role to user: {user.username}')
                else:
                    self.stdout.write(f'  ✅ User {user.username} already has Admin role')

            except UserProfile.DoesNotExist:
                # Create UserProfile if it doesn't exist for admin users
                profile = UserProfile.objects.create(
                    user=user,
                    first_name=user.first_name or 'Admin',
                    last_name=user.last_name or 'User',
                    email=user.email or f'{user.username}@jeticu.com',
                    status='active'
                )
                profile.roles.add(admin_role)
                fixed_count += 1
                self.stdout.write(f'  ✅ Created profile and added Admin role for user: {user.username}')

        self.stdout.write(f'  ✅ Fixed {fixed_count} existing admin users')