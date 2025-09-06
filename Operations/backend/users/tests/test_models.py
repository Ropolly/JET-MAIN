"""
Tests for users app models.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import UserProfile, Role, Permission, Department


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.department = Department.objects.create(
            name='Operations',
            description='Flight operations department'
        )
        
    def test_user_profile_creation(self):
        """Test UserProfile creation with valid data."""
        profile = UserProfile.objects.create(
            user=self.user,
            phone_number='+1234567890',
            address='123 Test St, Test City, TC 12345',
            emergency_contact='Jane Doe - +0987654321',
            department=self.department
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone_number, '+1234567890')
        self.assertTrue(profile.is_active)
        self.assertEqual(str(profile), f"{self.user.get_full_name() or self.user.username} Profile")
        
    def test_user_profile_str_method(self):
        """Test UserProfile string representation."""
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        
        profile = UserProfile.objects.create(
            user=self.user,
            department=self.department
        )
        
        self.assertEqual(str(profile), "John Doe Profile")


class RoleModelTest(TestCase):
    """Test cases for Role model."""
    
    def test_role_creation(self):
        """Test Role creation with valid data."""
        role = Role.objects.create(
            name='Pilot',
            description='Aircraft pilot role'
        )
        
        self.assertEqual(role.name, 'Pilot')
        self.assertEqual(role.description, 'Aircraft pilot role')
        self.assertTrue(role.is_active)
        self.assertEqual(str(role), 'Pilot')
        
    def test_role_unique_name(self):
        """Test that role names must be unique."""
        Role.objects.create(name='Pilot', description='First pilot role')
        
        with self.assertRaises(Exception):
            Role.objects.create(name='Pilot', description='Second pilot role')


class PermissionModelTest(TestCase):
    """Test cases for Permission model."""
    
    def test_permission_creation(self):
        """Test Permission creation with valid data."""
        permission = Permission.objects.create(
            name='view_trips',
            description='Can view trip information',
            resource='trips',
            action='view'
        )
        
        self.assertEqual(permission.name, 'view_trips')
        self.assertEqual(permission.resource, 'trips')
        self.assertEqual(permission.action, 'view')
        self.assertEqual(str(permission), 'view_trips')


class DepartmentModelTest(TestCase):
    """Test cases for Department model."""
    
    def test_department_creation(self):
        """Test Department creation with valid data."""
        department = Department.objects.create(
            name='Medical',
            description='Medical staff department',
            manager_email='manager@medical.com'
        )
        
        self.assertEqual(department.name, 'Medical')
        self.assertEqual(department.description, 'Medical staff department')
        self.assertEqual(department.manager_email, 'manager@medical.com')
        self.assertTrue(department.is_active)
        self.assertEqual(str(department), 'Medical')
        
    def test_department_unique_name(self):
        """Test that department names must be unique."""
        Department.objects.create(name='Operations', description='First ops dept')
        
        with self.assertRaises(Exception):
            Department.objects.create(name='Operations', description='Second ops dept')
