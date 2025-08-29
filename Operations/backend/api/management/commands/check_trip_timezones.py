from django.core.management.base import BaseCommand
from api.models import Trip, TripLine, Airport


class Command(BaseCommand):
    help = 'Check timezone data for a specific trip'

    def add_arguments(self, parser):
        parser.add_argument('trip_id', type=str, help='Trip ID to check')

    def handle(self, *args, **options):
        trip_id = options['trip_id']
        
        try:
            trip = Trip.objects.get(id=trip_id)
            self.stdout.write(f"Trip: {trip.trip_number}")
            
            trip_lines = trip.trip_lines.all()
            self.stdout.write(f"Found {trip_lines.count()} trip lines")
            
            for i, line in enumerate(trip_lines, 1):
                self.stdout.write(f"\n--- Trip Line {i} ---")
                
                # Check origin airport
                if line.origin_airport:
                    self.stdout.write(f"Origin: {line.origin_airport.name} ({line.origin_airport.ident})")
                    self.stdout.write(f"Origin timezone: {line.origin_airport.timezone or 'NOT SET'}")
                else:
                    self.stdout.write("Origin: NOT SET")
                
                # Check destination airport
                if line.destination_airport:
                    self.stdout.write(f"Destination: {line.destination_airport.name} ({line.destination_airport.ident})")
                    self.stdout.write(f"Destination timezone: {line.destination_airport.timezone or 'NOT SET'}")
                else:
                    self.stdout.write("Destination: NOT SET")
                
                # Check times
                self.stdout.write(f"Departure local: {line.departure_time_local}")
                self.stdout.write(f"Departure UTC: {line.departure_time_utc}")
                self.stdout.write(f"Arrival local: {line.arrival_time_local}")
                self.stdout.write(f"Arrival UTC: {line.arrival_time_utc}")
                
        except Trip.DoesNotExist:
            self.stdout.write(f"Trip {trip_id} not found")
        except Exception as e:
            self.stdout.write(f"Error: {str(e)}")