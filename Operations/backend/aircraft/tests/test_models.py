"""
Tests for aircraft app models.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from aircraft.models import Aircraft, MaintenanceLog


class AircraftModelTest(TestCase):
    """Test cases for Aircraft model."""
    
    def test_aircraft_creation(self):
        """Test Aircraft creation with valid data."""
        aircraft = Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Citation CJ3',
            manufacturer='Cessna',
            model='Citation CJ3',
            year_manufactured=2020,
            max_passengers=8,
            max_range_nm=2040,
            cruise_speed_kts=417,
            fuel_capacity_gallons=Decimal('1560.00'),
            empty_weight_lbs=Decimal('10500.00'),
            max_takeoff_weight_lbs=Decimal('17110.00')
        )
        
        self.assertEqual(aircraft.tail_number, 'N123AB')
        self.assertEqual(aircraft.aircraft_type, 'Citation CJ3')
        self.assertEqual(aircraft.manufacturer, 'Cessna')
        self.assertEqual(aircraft.max_passengers, 8)
        self.assertTrue(aircraft.is_active)
        self.assertEqual(str(aircraft), 'N123AB - Citation CJ3')
        
    def test_aircraft_tail_number_validation(self):
        """Test Aircraft tail number validation."""
        aircraft = Aircraft(
            tail_number='',  # Empty tail number
            aircraft_type='Test Type',
            manufacturer='Test Mfg'
        )
        
        with self.assertRaises(ValidationError):
            aircraft.full_clean()
            
    def test_aircraft_unique_tail_number(self):
        """Test that tail numbers must be unique."""
        Aircraft.objects.create(
            tail_number='N123AB',
            aircraft_type='Type 1',
            manufacturer='Mfg 1'
        )
        
        with self.assertRaises(Exception):
            Aircraft.objects.create(
                tail_number='N123AB',
                aircraft_type='Type 2',
                manufacturer='Mfg 2'
            )


class MaintenanceLogModelTest(TestCase):
    """Test cases for MaintenanceLog model."""
    
    def setUp(self):
        """Set up test data."""
        self.aircraft = Aircraft.objects.create(
            tail_number='N456CD',
            aircraft_type='King Air 350',
            manufacturer='Beechcraft',
            model='King Air 350'
        )
        
    def test_maintenance_log_creation(self):
        """Test MaintenanceLog creation with valid data."""
        log = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='inspection',
            description='100-hour inspection completed',
            performed_by='John Smith, A&P',
            cost=Decimal('2500.00'),
            hours_at_maintenance=Decimal('1250.5')
        )
        
        self.assertEqual(log.aircraft, self.aircraft)
        self.assertEqual(log.maintenance_type, 'inspection')
        self.assertEqual(log.description, '100-hour inspection completed')
        self.assertEqual(log.cost, Decimal('2500.00'))
        self.assertIsNotNone(log.date_performed)
        self.assertEqual(str(log), f'N456CD - inspection on {log.date_performed.strftime("%Y-%m-%d")}')
        
    def test_maintenance_log_aircraft_relationship(self):
        """Test MaintenanceLog aircraft relationship."""
        log1 = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='repair',
            description='Engine repair'
        )
        
        log2 = MaintenanceLog.objects.create(
            aircraft=self.aircraft,
            maintenance_type='inspection',
            description='Annual inspection'
        )
        
        # Test reverse relationship
        logs = self.aircraft.maintenance_logs.all()
        self.assertEqual(logs.count(), 2)
        self.assertIn(log1, logs)
        self.assertIn(log2, logs)
