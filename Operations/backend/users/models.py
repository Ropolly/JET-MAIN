from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel


class Permission(BaseModel):
    """Permission model for fine-grained access control."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Role(BaseModel):
    """Role model for grouping permissions."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Department(BaseModel):
    """Department model for organizational structure."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="departments")
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    """Extended user profile with additional fields and relationships."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department_ids = models.ManyToManyField(Department, related_name="users")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    
    # Role and department relationships
    roles = models.ManyToManyField(Role, related_name="users")
    departments = models.ManyToManyField(Department, related_name="department_users")
    
    # Additional metadata
    flags = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        """Return full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def has_permission(self, permission_name):
        """Check if user has a specific permission through roles."""
        return self.roles.filter(permissions__name=permission_name).exists()
    
    def get_all_permissions(self):
        """Get all permissions for this user through roles."""
        return Permission.objects.filter(roles__users=self).distinct()


class Staff(BaseModel):
    """Staff model for operational crew members."""
    contact = models.OneToOneField("contacts.Contact", on_delete=models.CASCADE, related_name="staff")
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['active']),
        ]
    
    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name}".strip() or str(self.contact_id)


class StaffRole(BaseModel):
    """Staff role model for operational positions."""
    code = models.CharField(max_length=32, unique=True)   # e.g., 'PIC', 'SIC', 'RN', 'PARAMEDIC'
    name = models.CharField(max_length=64)                # e.g., 'Pilot in Command'
    
    class Meta:
        indexes = [
            models.Index(fields=["code"]),
        ]
    
    def __str__(self):
        return self.code


class StaffRoleMembership(BaseModel):
    """Staff role membership with time periods."""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="role_memberships")
    role = models.ForeignKey(StaffRole, on_delete=models.PROTECT, related_name="memberships")
    start_on = models.DateField(null=True, blank=True)
    end_on = models.DateField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "role", "start_on", "end_on"],
                name="uniq_staff_role_interval"
            )
        ]
        indexes = [
            models.Index(fields=['staff', 'role']),
            models.Index(fields=['start_on', 'end_on']),
        ]
    
    def __str__(self):
        return f"{self.staff} - {self.role}"
