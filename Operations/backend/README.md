# JET ICU Operations Backend

This is the Django backend for the JET ICU Operations system, a management platform for a jet ambulance company.

## Project Structure

The backend is built with Django and Django REST Framework, following a **modular architecture** with domain-specific apps:

### Core Apps
- `users/` - User authentication, roles, permissions, profiles, departments
- `contacts/` - Contact management, FBOs, ground transportation services
- `airports/` - Airport data, weather services, distance calculations
- `aircraft/` - Aircraft management and maintenance logs
- `operations/` - Trip operations, quotes, passengers, patients, crew lines
- `documents/` - Document management, agreements, templates, access logging
- `finance/` - Transactions, invoices, payment methods, line items
- `common/` - Shared utilities, base models, permissions, middleware
- `backend/` - Project configuration and main URL routing

### Service Layer Architecture

Each app follows a clean architecture pattern with:
- **Models**: Data layer with proper relationships and validation
- **Services**: Business logic layer (`services/` directory in each app)
- **Serializers**: API data transformation with comprehensive validation
- **Views**: DRF ViewSets with custom actions and filtering
- **URLs**: Clean routing with DefaultRouter
- **Admin**: Django admin configurations
- **Tests**: Comprehensive test suites using Django TestCase

## Key Features

### Business Logic Services
- `TripService` - Trip creation, scheduling, time calculations
- `QuoteService` - Quote generation, pricing, approval workflows
- `DocumentService` - Document upload/download with access logging
- `PaymentProcessorService` - Multi-provider payment processing (Stripe, Square)
- `WeatherScrapingService` - Aviation weather data (METAR/TAF)
- `SchedulerService` - Background task scheduling and management

### Document Generation
- General Declaration (GenDec) for aviation authorities
- Customer and internal itineraries
- Quote documents with pricing breakdown
- Template-based document generation using python-docx

### Financial Processing
- Transaction management with audit trails
- Multi-provider payment processing
- Invoice generation and line item tracking
- Refund processing and payment method management

### Aviation-Specific Features
- Timezone-aware flight scheduling
- Distance calculations between airports
- Weather data integration
- Crew scheduling and management
- Patient transport coordination

## Setup Instructions

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

The API is available at `/api/` with modular endpoints organized by domain:

### User Management
- `/api/users/` - User profiles, authentication, departments
- `/api/auth/` - JWT token authentication endpoints

### Contact Management
- `/api/contacts/` - Contact information and relationships
- `/api/fbos/` - Fixed Base Operator (FBO) services
- `/api/grounds/` - Ground transportation services

### Aviation Operations
- `/api/airports/` - Airport data and weather information
- `/api/aircraft/` - Aircraft fleet management
- `/api/operations/trips/` - Trip planning and execution
- `/api/operations/quotes/` - Quote generation and management
- `/api/operations/passengers/` - Passenger information
- `/api/operations/crew-lines/` - Crew scheduling

### Document Management
- `/api/documents/` - Document upload, download, and access control
- `/api/documents/agreements/` - Legal agreements and signatures
- `/api/documents/templates/` - Document templates

### Financial Services
- `/api/finance/transactions/` - Payment processing and transaction history
- `/api/finance/invoices/` - Invoice generation and management
- `/api/finance/payment-methods/` - Payment method management

## Authentication

Authentication is handled via JWT (JSON Web Tokens):

- **Login**: `POST /api/auth/login/` with username and password
- **Token Refresh**: `POST /api/auth/token/refresh/` with refresh token
- **Logout**: `POST /api/auth/logout/` (blacklists the token)

Include the access token in the Authorization header:
```
Authorization: Bearer <your-access-token>
```

## Environment Configuration

The application uses environment variables for configuration. Create a `.env` file:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/jet_operations
# Or for development:
# DATABASE_URL=sqlite:///db.sqlite3

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=7  # days

# External API Keys (optional)
STRIPE_SECRET_KEY=sk_test_...
SQUARE_ACCESS_TOKEN=sandbox-sq0atb-...
SQUARE_SANDBOX=True

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Business Process Flow

### 1. Quote Generation
- Customer contact creates initial quote request
- System calculates pricing based on aircraft type, distance, medical requirements
- Quote document generated and sent to customer

### 2. Agreement and Payment
- Customer accepts quote and signs digital agreement
- Payment processing through integrated providers (Stripe/Square)
- Transaction tracking with audit trail

### 3. Trip Planning
- Trip creation with passenger/patient information
- Crew assignment and scheduling
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
