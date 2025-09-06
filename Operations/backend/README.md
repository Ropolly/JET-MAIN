# JET ICU Operations Backend

A Django REST API backend for managing air medical transport operations, built with a **clean modular architecture** for scalability and maintainability.

## Architecture Overview

This backend follows a **modular Django app structure** with domain-specific apps, each handling a specific business area:

### Domain Apps

- **`users/`** - Authentication, user profiles, roles, permissions, departments
- **`contacts/`** - Contact management, FBOs, ground service providers
- **`airports/`** - Airport data, weather services, distance calculations
- **`aircraft/`** - Aircraft management, maintenance logs, specifications
- **`operations/`** - Trip operations, quotes, passengers, patients, crew assignments
- **`documents/`** - Document management, agreements, templates, access logging
- **`finance/`** - Financial transactions, invoices, payment methods, line items
- **`common/`** - Shared utilities, base models, permissions, middleware

### Service Layer Pattern

Each app implements a **service layer** to separate business logic from models and views:

```python
# Example: operations/services/trip_service.py
class TripService:
    @staticmethod
    def create_trip(trip_data):
        # Business logic for trip creation
        pass
    
    @staticmethod
    def calculate_flight_time(origin, destination):
        # Flight time calculation logic
        pass
```

## Technology Stack

- **Django 5.2** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **JWT Authentication** - Token-based auth with rotation
- **python-docx** - Document generation
- **Celery** - Background task processing (optional)

## Environment Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+ (optional, for caching)

### Installation

1. **Clone and setup virtual environment:**
```bash
git clone <repository-url>
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment configuration:**
Create a `.env` file in the project root:
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/jeticu_db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=3600  # 1 hour in seconds
JWT_REFRESH_TOKEN_LIFETIME=604800  # 7 days in seconds

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# API Keys (for external services)
STRIPE_SECRET_KEY=sk_test_...
SQUARE_ACCESS_TOKEN=sandbox-sq0atb-...
PAYPAL_CLIENT_ID=your-paypal-client-id
```

4. **Database setup:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Run development server:**
```bash
python manage.py runserver
```

## API Endpoints

The API is organized by domain with consistent RESTful patterns:

### Authentication
- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

### Users & Authentication
- `GET|POST /api/users/profiles/` - User profiles
- `GET|POST /api/users/roles/` - User roles
- `GET|POST /api/users/permissions/` - Permissions
- `GET|POST /api/users/departments/` - Departments

### Contacts
- `GET|POST /api/contacts/contacts/` - Contact management
- `GET|POST /api/contacts/fbos/` - FBO services
- `GET|POST /api/contacts/ground/` - Ground service providers

### Airports
- `GET|POST /api/airports/airports/` - Airport data
- `GET|POST /api/airports/weather/` - Weather information
- `GET /api/airports/distance/` - Distance calculations

### Aircraft
- `GET|POST /api/aircraft/aircraft/` - Aircraft fleet
- `GET|POST /api/aircraft/maintenance/` - Maintenance logs

### Operations
- `GET|POST /api/operations/trips/` - Trip management
- `GET|POST /api/operations/quotes/` - Quote generation
- `GET|POST /api/operations/passengers/` - Passenger management
- `GET|POST /api/operations/patients/` - Patient information
- `GET|POST /api/operations/crew/` - Crew assignments

### Documents
- `GET|POST /api/documents/documents/` - Document management
- `GET|POST /api/documents/agreements/` - Agreement templates
- `POST /api/documents/generate/` - Document generation

### Finance
- `GET|POST /api/finance/transactions/` - Financial transactions
- `GET|POST /api/finance/invoices/` - Invoice management
- `GET|POST /api/finance/payments/` - Payment processing

## Business Flow

### 1. Quote Generation
```python
# Create a quote for a medical transport
quote_data = {
    "contact_id": "123",
    "pickup_airport": "KJFK",
    "dropoff_airport": "KLAX",
    "aircraft_type": "Citation CJ3",
    "medical_team": "RN/Paramedic",
    "departure_date": "2024-01-15T10:00:00Z"
}
response = requests.post("/api/operations/quotes/", data=quote_data)
```

### 2. Trip Creation & Management
```python
# Convert approved quote to trip
trip_data = {
    "quote_id": "456",
    "aircraft_id": "789",
    "crew_assignments": [...],
    "patient_info": {...}
}
response = requests.post("/api/operations/trips/", data=trip_data)
```

### 3. Document Generation
```python
# Generate General Declaration
doc_data = {
    "trip_id": "789",
    "template_type": "general_declaration"
}
response = requests.post("/api/documents/generate/", data=doc_data)
```
- Flight legs with automatic time zone calculations
- Weather data integration for flight planning

### 4. Document Generation
- General Declaration (GenDec) for aviation authorities
- Customer and internal itineraries
- Crew briefing documents

### 5. Operations Execution
- Real-time trip monitoring
- Document access logging
- Post-flight reporting and billing

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test documents
python manage.py test finance
python manage.py test operations

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Migration from Legacy System

This system has been refactored from a monolithic architecture to a modular design. See `MIGRATION_GUIDE.md` for detailed migration instructions and data transfer procedures.

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

The API follows RESTful conventions with consistent response formats and comprehensive error handling.
