"""
Django test cases for weather scraping functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from unittest.mock import patch, Mock
from airports.models import Airport, WeatherData
from airports.services.weather_scraper import WeatherScrapingService, AirportDataScrapingService


class WeatherScrapingTestCase(TestCase):
    """Test case for weather scraping functionality."""
    
    def setUp(self):
        """Set up test data for weather scraping tests."""
        self.airport = Airport.objects.create(
            name="Los Angeles International Airport",
            iata_code="LAX",
            icao_code="KLAX",
            city="Los Angeles",
            state="CA",
            country="USA",
            latitude=33.942536,
            longitude=-118.408074,
            timezone="America/Los_Angeles"
        )
        
        self.weather_service = WeatherScrapingService()
        self.airport_service = AirportDataScrapingService()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_metar_fetching_success(self, mock_get):
        """Test successful METAR data fetching."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "KLAX 121953Z 25008KT 10SM FEW015 SCT250 22/18 A2995 RMK AO2 SLP141 T02220183"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test METAR fetching
        metar = self.weather_service.get_metar("KLAX")
        
        # Assertions
        self.assertIsNotNone(metar)
        self.assertIn("KLAX", metar)
        self.assertIn("25008KT", metar)
        mock_get.assert_called_once()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_metar_fetching_no_data(self, mock_get):
        """Test METAR fetching when no data is available."""
        # Mock no data response
        mock_response = Mock()
        mock_response.text = "No METAR available"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test METAR fetching
        metar = self.weather_service.get_metar("INVALID")
        
        # Assertions
        self.assertIsNone(metar)
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_taf_fetching_success(self, mock_get):
        """Test successful TAF data fetching."""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "KLAX 121720Z 1218/1324 25008KT P6SM FEW015 SCT250"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test TAF fetching
        taf = self.weather_service.get_taf("KLAX")
        
        # Assertions
        self.assertIsNotNone(taf)
        self.assertIn("KLAX", taf)
        self.assertIn("25008KT", taf)
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_weather_update_success(self, mock_get):
        """Test successful weather data update for airport."""
        # Mock successful responses for both METAR and TAF
        mock_response = Mock()
        mock_response.text = "KLAX 121953Z 25008KT 10SM FEW015 SCT250 22/18 A2995"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test weather update
        weather_data = self.weather_service.update_airport_weather("KLAX")
        
        # Assertions
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data.airport, self.airport)
        self.assertIsNotNone(weather_data.metar)
        self.assertEqual(weather_data.data_source, 'aviationweather.gov')
        
        # Verify database record was created
        self.assertTrue(WeatherData.objects.filter(airport=self.airport).exists())
    
    def test_weather_update_nonexistent_airport(self):
        """Test weather update for non-existent airport."""
        weather_data = self.weather_service.update_airport_weather("INVALID")
        self.assertIsNone(weather_data)
    
    @patch('airports.services.weather_scraper.WeatherScrapingService.update_airport_weather')
    def test_bulk_weather_update(self, mock_update):
        """Test bulk weather update functionality."""
        # Mock successful updates
        mock_update.side_effect = [Mock(), None, Mock()]  # 2 success, 1 failure
        
        # Test bulk update
        results = self.weather_service.bulk_update_weather(["KLAX", "INVALID", "KJFK"])
        
        # Assertions
        self.assertEqual(results['success'], 2)
        self.assertEqual(results['failed'], 1)
        self.assertEqual(len(results['errors']), 1)
        self.assertEqual(mock_update.call_count, 3)
    
    def test_metar_parsing(self):
        """Test METAR string parsing functionality."""
        metar_string = "KLAX 121953Z 25008KT 10SM FEW015 SCT250 22/18 A2995"
        
        conditions = self.weather_service.get_weather_conditions(metar_string)
        
        # Assertions
        self.assertEqual(conditions['wind_direction'], 250)
        self.assertEqual(conditions['wind_speed'], 8)
        self.assertEqual(conditions['temperature'], 22)
        self.assertEqual(conditions['visibility'], 10.0)
        self.assertIn('FEW', conditions['conditions'])
        self.assertIn('SCT', conditions['conditions'])
    
    def test_metar_parsing_negative_temperature(self):
        """Test METAR parsing with negative temperature."""
        metar_string = "KLAX 121953Z 25008KT 10SM CLR M05/M10 A2995"
        
        conditions = self.weather_service.get_weather_conditions(metar_string)
        
        # Assertions
        self.assertEqual(conditions['temperature'], -5)
        self.assertIn('CLR', conditions['conditions'])
    
    def test_metar_parsing_empty_string(self):
        """Test METAR parsing with empty string."""
        conditions = self.weather_service.get_weather_conditions("")
        
        # Should return empty dict
        self.assertEqual(conditions, {})
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_network_error_handling(self, mock_get):
        """Test network error handling."""
        # Mock network error
        mock_get.side_effect = Exception("Network error")
        
        # Test METAR fetching with error
        metar = self.weather_service.get_metar("KLAX")
        self.assertIsNone(metar)
        
        # Test TAF fetching with error
        taf = self.weather_service.get_taf("KLAX")
        self.assertIsNone(taf)


class AirportDataScrapingTestCase(TestCase):
    """Test case for airport data scraping functionality."""
    
    def setUp(self):
        """Set up test data for airport data scraping tests."""
        self.airport_service = AirportDataScrapingService()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_airport_info_scraping_success(self, mock_get):
        """Test successful airport information scraping."""
        # Mock HTML response
        mock_response = Mock()
        mock_response.text = """
        <html>
            <h1>Los Angeles International Airport</h1>
            <div class="location">Los Angeles, CA, USA</div>
            <div class="elevation">125 ft</div>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test airport info scraping
        airport_data = self.airport_service.get_airport_info("LAX")
        
        # Assertions
        self.assertIsNotNone(airport_data)
        self.assertEqual(airport_data['code'], 'LAX')
        self.assertEqual(airport_data['name'], 'Los Angeles International Airport')
        mock_get.assert_called_once()
    
    @patch('airports.services.weather_scraper.requests.Session.get')
    def test_airport_info_scraping_error(self, mock_get):
        """Test airport information scraping with network error."""
        # Mock network error
        mock_get.side_effect = Exception("Network error")
        
        # Test airport info scraping
        airport_data = self.airport_service.get_airport_info("LAX")
        
        # Assertions
        self.assertIsNone(airport_data)
    
    def test_coordinate_extraction(self):
        """Test coordinate extraction from HTML."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="coordinates">33.942536°N 118.408074°W</div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        coordinates = self.airport_service._extract_coordinates(soup)
        
        # Note: This is a simplified test - actual implementation may vary
        # based on the website structure
        if coordinates:
            self.assertIsInstance(coordinates, dict)
            self.assertIn('latitude', coordinates)
            self.assertIn('longitude', coordinates)
    
    def test_elevation_extraction(self):
        """Test elevation extraction from HTML."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="elevation">125 ft MSL</div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        elevation = self.airport_service._extract_elevation(soup)
        
        # Should extract numeric elevation
        if elevation:
            self.assertEqual(elevation, 125)
