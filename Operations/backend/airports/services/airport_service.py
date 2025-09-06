"""
Airport service module containing business logic for airport operations.
"""
from django.db import transaction
from django.utils import timezone
from typing import List, Optional, Dict, Any
from datetime import datetime
import math

from ..models import Airport, WeatherData
from common.timezone_utils import convert_local_to_utc, convert_utc_to_local


class AirportService:
    """Service class for airport-related business logic."""
    
    @staticmethod
    def calculate_distance(airport1: Airport, airport2: Airport) -> float:
        """
        Calculate great circle distance between two airports in nautical miles.
        
        Args:
            airport1: First Airport instance
            airport2: Second Airport instance
            
        Returns:
            Distance in nautical miles
        """
        return airport1.calculate_distance_to(airport2)
    
    @staticmethod
    def convert_to_utc(local_datetime: datetime, airport_timezone: str) -> datetime:
        """
        Convert local airport time to UTC.
        
        Args:
            local_datetime: Local datetime
            airport_timezone: Airport timezone string
            
        Returns:
            UTC datetime
        """
        return convert_local_to_utc(local_datetime, airport_timezone)
    
    @staticmethod
    def convert_from_utc(utc_datetime: datetime, airport_timezone: str) -> datetime:
        """
        Convert UTC time to local airport time.
        
        Args:
            utc_datetime: UTC datetime
            airport_timezone: Airport timezone string
            
        Returns:
            Local datetime
        """
        return convert_utc_to_local(utc_datetime, airport_timezone)
    
    @staticmethod
    def find_airports_by_code(code: str) -> List[Airport]:
        """
        Find airports by ICAO, IATA, or identifier code.
        
        Args:
            code: Airport code to search for
            
        Returns:
            List of matching airports
        """
        code_upper = code.upper()
        
        airports = Airport.objects.filter(
            models.Q(icao_code__iexact=code_upper) |
            models.Q(iata_code__iexact=code_upper) |
            models.Q(ident__iexact=code_upper)
        ).distinct()
        
        return list(airports)
    
    @staticmethod
    def search_airports(query: str, limit: int = 20) -> List[Airport]:
        """
        Search airports by name, code, or location.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching airports
        """
        from django.db import models
        
        query_upper = query.upper()
        
        airports = Airport.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(municipality__icontains=query) |
            models.Q(icao_code__icontains=query_upper) |
            models.Q(iata_code__icontains=query_upper) |
            models.Q(ident__icontains=query_upper)
        ).distinct()[:limit]
        
        return list(airports)
    
    @staticmethod
    def get_airports_in_region(country: str, region: Optional[str] = None) -> List[Airport]:
        """
        Get airports in a specific country or region.
        
        Args:
            country: ISO country code
            region: Optional ISO region code
            
        Returns:
            List of airports in the region
        """
        queryset = Airport.objects.filter(iso_country=country)
        
        if region:
            queryset = queryset.filter(iso_region=region)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def calculate_flight_path(
        origin: Airport,
        destination: Airport,
        waypoints: Optional[List[Airport]] = None
    ) -> Dict[str, Any]:
        """
        Calculate flight path information between airports.
        
        Args:
            origin: Origin airport
            destination: Destination airport
            waypoints: Optional list of waypoint airports
            
        Returns:
            Dictionary with flight path information
        """
        total_distance = 0
        legs = []
        
        if waypoints:
            # Calculate distance through waypoints
            current_airport = origin
            
            for waypoint in waypoints:
                leg_distance = AirportService.calculate_distance(current_airport, waypoint)
                legs.append({
                    'from': current_airport,
                    'to': waypoint,
                    'distance_nm': leg_distance
                })
                total_distance += leg_distance
                current_airport = waypoint
            
            # Final leg to destination
            final_leg_distance = AirportService.calculate_distance(current_airport, destination)
            legs.append({
                'from': current_airport,
                'to': destination,
                'distance_nm': final_leg_distance
            })
            total_distance += final_leg_distance
        else:
            # Direct flight
            total_distance = AirportService.calculate_distance(origin, destination)
            legs.append({
                'from': origin,
                'to': destination,
                'distance_nm': total_distance
            })
        
        return {
            'origin': origin,
            'destination': destination,
            'waypoints': waypoints or [],
            'legs': legs,
            'total_distance_nm': total_distance,
            'estimated_flight_time_hours': AirportService._estimate_flight_time(total_distance)
        }
    
    @staticmethod
    def _estimate_flight_time(distance_nm: float, aircraft_speed_knots: float = 400) -> float:
        """
        Estimate flight time based on distance and average speed.
        
        Args:
            distance_nm: Distance in nautical miles
            aircraft_speed_knots: Average aircraft speed in knots
            
        Returns:
            Estimated flight time in hours
        """
        return distance_nm / aircraft_speed_knots


class WeatherService:
    """Service class for weather-related operations."""
    
    @staticmethod
    def get_current_weather(airport: Airport) -> Optional[WeatherData]:
        """
        Get the most recent weather data for an airport.
        
        Args:
            airport: Airport instance
            
        Returns:
            Most recent WeatherData or None
        """
        return airport.weather_data.first()  # Already ordered by -observation_time
    
    @staticmethod
    def get_weather_history(
        airport: Airport,
        hours_back: int = 24
    ) -> List[WeatherData]:
        """
        Get weather history for an airport.
        
        Args:
            airport: Airport instance
            hours_back: Number of hours to look back
            
        Returns:
            List of WeatherData instances
        """
        cutoff_time = timezone.now() - timezone.timedelta(hours=hours_back)
        
        return list(airport.weather_data.filter(
            observation_time__gte=cutoff_time
        ))
    
    @staticmethod
    def store_weather_data(
        airport: Airport,
        weather_info: Dict[str, Any],
        source: str = 'METAR'
    ) -> WeatherData:
        """
        Store weather data for an airport.
        
        Args:
            airport: Airport instance
            weather_info: Dictionary with weather information
            source: Weather data source
            
        Returns:
            Created WeatherData instance
        """
        return WeatherData.objects.create(
            airport=airport,
            temperature_celsius=weather_info.get('temperature_celsius'),
            wind_speed_knots=weather_info.get('wind_speed_knots'),
            wind_direction_degrees=weather_info.get('wind_direction_degrees'),
            visibility_miles=weather_info.get('visibility_miles'),
            barometric_pressure_inhg=weather_info.get('barometric_pressure_inhg'),
            humidity_percent=weather_info.get('humidity_percent'),
            conditions=weather_info.get('conditions'),
            ceiling_feet=weather_info.get('ceiling_feet'),
            observation_time=weather_info.get('observation_time', timezone.now()),
            source=source,
            raw_data=weather_info.get('raw_data')
        )
    
    @staticmethod
    def analyze_weather_conditions(weather_data: WeatherData) -> Dict[str, Any]:
        """
        Analyze weather conditions for flight operations.
        
        Args:
            weather_data: WeatherData instance
            
        Returns:
            Dictionary with weather analysis
        """
        analysis = {
            'suitable_for_flight': True,
            'warnings': [],
            'conditions_summary': weather_data.conditions or 'Unknown'
        }
        
        # Check visibility
        if weather_data.visibility_miles and weather_data.visibility_miles < 3:
            analysis['suitable_for_flight'] = False
            analysis['warnings'].append('Low visibility')
        
        # Check wind conditions
        if weather_data.wind_speed_knots and weather_data.wind_speed_knots > 35:
            analysis['suitable_for_flight'] = False
            analysis['warnings'].append('High winds')
        
        # Check ceiling
        if weather_data.ceiling_feet and weather_data.ceiling_feet < 1000:
            analysis['warnings'].append('Low ceiling')
        
        # Check for severe weather conditions
        severe_conditions = ['thunderstorm', 'tornado', 'hail', 'freezing']
        if weather_data.conditions:
            for condition in severe_conditions:
                if condition.lower() in weather_data.conditions.lower():
                    analysis['suitable_for_flight'] = False
                    analysis['warnings'].append(f'Severe weather: {condition}')
        
        return analysis
