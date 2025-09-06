"""
Weather Data Scraper Service for Airport Operations

Moved from utils/webscraping/scrapers.py to airports/services/weather_scraper.py
This service handles fetching weather data for flight planning.
"""

import requests
from bs4 import BeautifulSoup
import logging
from django.utils import timezone
from ..models import Airport, WeatherData

logger = logging.getLogger(__name__)


class WeatherScrapingService:
    """
    Service for fetching weather data for flight planning
    """
    
    def __init__(self, base_url="https://aviationweather.gov"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JET-ICU-Operations/1.0 (Weather Data Service)'
        })
    
    def get_metar(self, airport_code):
        """
        Fetch METAR (Meteorological Aerodrome Report) for a specific airport
        
        Args:
            airport_code: ICAO or IATA airport code
            
        Returns:
            str: METAR data or None if error
        """
        try:
            url = f"{self.base_url}/metar/data?ids={airport_code}&format=raw"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse the response to extract METAR data
            metar_data = response.text.strip()
            
            if metar_data and not metar_data.startswith('No METAR'):
                logger.info(f"Successfully fetched METAR for {airport_code}")
                return metar_data
            else:
                logger.warning(f"No METAR data available for {airport_code}")
                return None
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching METAR for {airport_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching METAR for {airport_code}: {str(e)}")
            return None
    
    def get_taf(self, airport_code):
        """
        Fetch TAF (Terminal Aerodrome Forecast) for a specific airport
        
        Args:
            airport_code: ICAO or IATA airport code
            
        Returns:
            str: TAF data or None if error
        """
        try:
            url = f"{self.base_url}/taf/data?ids={airport_code}&format=raw"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse the response to extract TAF data
            taf_data = response.text.strip()
            
            if taf_data and not taf_data.startswith('No TAF'):
                logger.info(f"Successfully fetched TAF for {airport_code}")
                return taf_data
            else:
                logger.warning(f"No TAF data available for {airport_code}")
                return None
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching TAF for {airport_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching TAF for {airport_code}: {str(e)}")
            return None
    
    def update_airport_weather(self, airport_code):
        """
        Update weather data for a specific airport and store in database
        
        Args:
            airport_code: ICAO or IATA airport code
            
        Returns:
            WeatherData instance or None if error
        """
        try:
            # Try to find airport by ICAO code first, then IATA
            airport = None
            try:
                airport = Airport.objects.get(icao_code=airport_code.upper())
            except Airport.DoesNotExist:
                try:
                    airport = Airport.objects.get(iata_code=airport_code.upper())
                except Airport.DoesNotExist:
                    logger.error(f"Airport not found: {airport_code}")
                    return None
            
            # Fetch weather data
            metar = self.get_metar(airport_code)
            taf = self.get_taf(airport_code)
            
            if not metar and not taf:
                logger.warning(f"No weather data available for {airport_code}")
                return None
            
            # Create or update weather data record
            weather_data, created = WeatherData.objects.update_or_create(
                airport=airport,
                defaults={
                    'metar': metar,
                    'taf': taf,
                    'last_updated': timezone.now(),
                    'data_source': 'aviationweather.gov'
                }
            )
            
            action = "Created" if created else "Updated"
            logger.info(f"{action} weather data for {airport.icao_code}")
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Error updating weather data for {airport_code}: {str(e)}")
            return None
    
    def bulk_update_weather(self, airport_codes):
        """
        Update weather data for multiple airports
        
        Args:
            airport_codes: List of ICAO or IATA airport codes
            
        Returns:
            dict: Results summary with success/failure counts
        """
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for airport_code in airport_codes:
            try:
                weather_data = self.update_airport_weather(airport_code)
                if weather_data:
                    results['success'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to update {airport_code}")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error updating {airport_code}: {str(e)}")
        
        logger.info(f"Bulk weather update completed: {results['success']} success, {results['failed']} failed")
        return results
    
    def get_weather_conditions(self, metar_string):
        """
        Parse METAR string to extract basic weather conditions
        
        Args:
            metar_string: Raw METAR string
            
        Returns:
            dict: Parsed weather conditions
        """
        if not metar_string:
            return {}
        
        conditions = {
            'visibility': None,
            'wind_speed': None,
            'wind_direction': None,
            'temperature': None,
            'conditions': []
        }
        
        try:
            parts = metar_string.split()
            
            for part in parts:
                # Wind information (e.g., 27008KT)
                if 'KT' in part and len(part) >= 5:
                    try:
                        wind_dir = part[:3]
                        wind_speed = part[3:5]
                        if wind_dir.isdigit():
                            conditions['wind_direction'] = int(wind_dir)
                        if wind_speed.isdigit():
                            conditions['wind_speed'] = int(wind_speed)
                    except (ValueError, IndexError):
                        pass
                
                # Temperature/Dewpoint (e.g., M02/M08)
                if '/' in part and len(part) <= 7:
                    try:
                        temp_part = part.split('/')[0]
                        if temp_part.startswith('M'):
                            temp = -int(temp_part[1:])
                        else:
                            temp = int(temp_part)
                        conditions['temperature'] = temp
                    except (ValueError, IndexError):
                        pass
                
                # Visibility (e.g., 10SM)
                if 'SM' in part:
                    try:
                        vis = part.replace('SM', '')
                        conditions['visibility'] = float(vis)
                    except ValueError:
                        pass
                
                # Weather conditions
                weather_codes = ['RA', 'SN', 'FG', 'BR', 'OVC', 'BKN', 'SCT', 'FEW', 'CLR']
                for code in weather_codes:
                    if code in part:
                        conditions['conditions'].append(code)
            
        except Exception as e:
            logger.error(f"Error parsing METAR: {str(e)}")
        
        return conditions


class AirportDataScrapingService:
    """
    Service for fetching airport data from public sources
    """
    
    def __init__(self, base_url="https://www.airport-data.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JET-ICU-Operations/1.0 (Airport Data Service)'
        })
        
    def get_airport_info(self, airport_code):
        """
        Fetch information about a specific airport by its IATA/ICAO code
        
        Args:
            airport_code: IATA or ICAO airport code
            
        Returns:
            dict: Airport information or None if error
        """
        try:
            url = f"{self.base_url}/airports/{airport_code}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract airport data (this is a simplified example)
            airport_data = {
                'code': airport_code.upper(),
                'name': self._extract_name(soup),
                'location': self._extract_location(soup),
                'elevation': self._extract_elevation(soup),
                'coordinates': self._extract_coordinates(soup),
                'runways': self._extract_runways(soup)
            }
            
            logger.info(f"Successfully scraped airport data for {airport_code}")
            return airport_data
            
        except requests.RequestException as e:
            logger.error(f"Network error fetching airport data for {airport_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching airport data for {airport_code}: {str(e)}")
            return None
    
    def _extract_name(self, soup):
        """Extract airport name from soup"""
        try:
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.text.strip()
        except Exception:
            pass
        return None
    
    def _extract_location(self, soup):
        """Extract airport location from soup"""
        try:
            # Look for location information in various possible elements
            location_selectors = [
                '.airport-location',
                '.location',
                'td:contains("Location")',
                'th:contains("Location")'
            ]
            
            for selector in location_selectors:
                element = soup.select_one(selector)
                if element:
                    return element.text.strip()
        except Exception:
            pass
        return "Location data not available"
    
    def _extract_elevation(self, soup):
        """Extract airport elevation from soup"""
        try:
            # Look for elevation information
            elevation_selectors = [
                '.elevation',
                'td:contains("Elevation")',
                'th:contains("Elevation")'
            ]
            
            for selector in elevation_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.text.strip()
                    # Extract numeric elevation
                    import re
                    match = re.search(r'(\d+)', text)
                    if match:
                        return int(match.group(1))
        except Exception:
            pass
        return None
    
    def _extract_coordinates(self, soup):
        """Extract airport coordinates from soup"""
        try:
            # Look for coordinate information
            coord_selectors = [
                '.coordinates',
                'td:contains("Coordinates")',
                'th:contains("Coordinates")'
            ]
            
            for selector in coord_selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.text.strip()
                    # Parse coordinates (simplified)
                    import re
                    lat_match = re.search(r'(\d+\.?\d*)[°\s]*N', text)
                    lon_match = re.search(r'(\d+\.?\d*)[°\s]*W', text)
                    
                    if lat_match and lon_match:
                        return {
                            'latitude': float(lat_match.group(1)),
                            'longitude': -float(lon_match.group(1))  # West is negative
                        }
        except Exception:
            pass
        return None
    
    def _extract_runways(self, soup):
        """Extract runway information from soup"""
        try:
            # Look for runway information
            runway_selectors = [
                '.runways',
                'td:contains("Runway")',
                'th:contains("Runway")'
            ]
            
            runways = []
            for selector in runway_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.text.strip()
                    if text and 'runway' in text.lower():
                        runways.append(text)
            
            return runways if runways else ["Runway data not available"]
        except Exception:
            pass
        return ["Runway data not available"]


# Convenience functions for backward compatibility
def get_metar(airport_code):
    """Get METAR data for an airport"""
    service = WeatherScrapingService()
    return service.get_metar(airport_code)


def get_taf(airport_code):
    """Get TAF data for an airport"""
    service = WeatherScrapingService()
    return service.get_taf(airport_code)


def update_airport_weather(airport_code):
    """Update weather data for an airport"""
    service = WeatherScrapingService()
    return service.update_airport_weather(airport_code)
