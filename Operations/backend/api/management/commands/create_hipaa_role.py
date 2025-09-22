"""
Django management command to create the hipaa_authorized role.
Run with: python manage.py create_hipaa_role
"""

from django.core.management.base import BaseCommand
from api.models import Role


class Command(BaseCommand):
    help = 'Create the hipaa_authorized role for HIPAA-protected endpoints'

    def handle(self, *args, **options):
        role_name = 'hipaa_authorized'
        
        # Check if role already exists
        role, created = Role.objects.get_or_create(
            name=role_name,
            defaults={
                'description': 'Users with this role can access HIPAA-protected patient data and endpoints. '
                              'This role should only be assigned to authorized personnel who have completed '
                              'HIPAA training and are authorized to handle protected health information (PHI).'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created role: {role_name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Role already exists: {role_name}')
            )
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Role ID: {role.id}\n'
                f'Description: {role.description}'
            )
        )
