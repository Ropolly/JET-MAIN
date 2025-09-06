# JET ICU Operations Backend Architecture

## System Overview

The JET ICU Operations Backend is a Django REST API built with a **modular architecture** that separates concerns into domain-specific applications. This design promotes maintainability, scalability, and team collaboration.

```
┌─────────────────────────────────────────────────────────────────┐
│                    JET ICU Operations Backend                    │
├─────────────────────────────────────────────────────────────────┤
│                        API Gateway                              │
│                    (Django + DRF)                              │
├─────────────────────────────────────────────────────────────────┤
│  users/   │ contacts/ │ airports/ │ aircraft/ │ operations/     │
│  auth &   │ customer  │ airport   │ fleet     │ trip mgmt      │
│  perms    │ mgmt      │ data      │ mgmt      │ & quotes       │
├───────────┼───────────┼───────────┼───────────┼────────────────┤
│ documents/│ finance/  │ common/   │           │                │
│ doc gen   │ billing   │ shared    │           │                │
│ & mgmt    │ & pay     │ utils     │           │                │
├─────────────────────────────────────────────────────────────────┤
│                    Service Layer                                │
│              (Business Logic & External APIs)                   │
├─────────────────────────────────────────────────────────────────┤
│                    Data Layer                                   │
│                 PostgreSQL + Redis                              │
└─────────────────────────────────────────────────────────────────┘
```

## Domain Applications

### 🔐 **users/** - Authentication & Authorization
**Purpose**: Manages user authentication, profiles, roles, and permissions

**Key Models**:
- `UserProfile` - Extended user information with department, contact details
- `Role` - User roles (Pilot, Dispatcher, Medical Staff, Admin)
- `Permission` - Granular permissions for resources and actions
- `Department` - Organizational departments

**Services**:
- User authentication and JWT token management
- Role-based access control (RBAC)
- Permission validation

**API Endpoints**:
- `/api/users/profiles/` - User profile management
- `/api/users/roles/` - Role assignment
- `/api/users/permissions/` - Permission management

---

### 👥 **contacts/** - Contact Management
**Purpose**: Manages all external contacts including customers, FBOs, and ground services

**Key Models**:
- `Contact` - General contact information for customers and vendors
- `FBO` - Fixed Base Operator services at airports
- `Ground` - Ground handling service providers

**Services**:
- Contact relationship management
- Service provider directory
- Communication history tracking

**API Endpoints**:
- `/api/contacts/contacts/` - Customer and vendor contacts
- `/api/contacts/fbos/` - FBO service providers
- `/api/contacts/ground/` - Ground handling services

---

### ✈️ **airports/** - Airport Data & Weather
**Purpose**: Manages airport information, weather data, and flight planning utilities

**Key Models**:
- `Airport` - Airport master data with ICAO/IATA codes, coordinates
- `WeatherData` - METAR/TAF weather information

**Services**:
- `WeatherScrapingService` - Fetches real-time weather data
- `AirportDataScrapingService` - Updates airport information
- Distance and flight time calculations

**API Endpoints**:
- `/api/airports/airports/` - Airport directory
- `/api/airports/weather/` - Weather information
- `/api/airports/distance/` - Distance calculations

---

### 🛩️ **aircraft/** - Fleet Management
**Purpose**: Manages aircraft fleet, specifications, and maintenance

**Key Models**:
- `Aircraft` - Aircraft registry with specifications and capabilities
- `MaintenanceLog` - Maintenance history and scheduling

**Services**:
- Fleet availability tracking
- Maintenance scheduling
- Aircraft performance calculations

**API Endpoints**:
- `/api/aircraft/aircraft/` - Fleet management
- `/api/aircraft/maintenance/` - Maintenance tracking

---

### 🚁 **operations/** - Trip Operations & Quotes
**Purpose**: Core business operations including trip management, quotes, and crew scheduling

**Key Models**:
- `Trip` - Flight operations with legs, crew, and passengers
- `Quote` - Price quotes for potential trips
- `Patient` - Medical patient information for air ambulance
- `Passenger` - General passenger manifest
- `CrewLine` - Crew assignments and scheduling

**Services**:
- `TripService` - Trip creation, scheduling, and management
- `QuoteService` - Quote generation and pricing
- `PatientService` - Medical patient handling
- `CrewService` - Crew scheduling and assignments

**API Endpoints**:
- `/api/operations/trips/` - Trip management
- `/api/operations/quotes/` - Quote generation
- `/api/operations/patients/` - Patient information
- `/api/operations/crew/` - Crew scheduling

---

### 📄 **documents/** - Document Management
**Purpose**: Handles document generation, storage, and access control

**Key Models**:
- `Document` - Document metadata and file management
- `Agreement` - Contract templates and signed agreements
- `DocumentAccess` - Access logging and permissions

**Services**:
- `DocumentGenerationService` - Generates GenDec, itineraries, quotes
- `DocumentService` - File management and access control
- Template management for various document types

**API Endpoints**:
- `/api/documents/documents/` - Document library
- `/api/documents/agreements/` - Contract management
- `/api/documents/generate/` - Document generation

---

### 💰 **finance/** - Financial Management
**Purpose**: Manages billing, payments, and financial transactions

**Key Models**:
- `Transaction` - Financial transaction records
- `Invoice` - Billing and invoicing
- `PaymentMethod` - Customer payment methods
- `LineItem` - Detailed billing line items

**Services**:
- `PaymentProcessorService` - Stripe, Square, PayPal integration
- `FinanceService` - Billing and invoice management
- Revenue reporting and analytics

**API Endpoints**:
- `/api/finance/transactions/` - Transaction history
- `/api/finance/invoices/` - Invoice management
- `/api/finance/payments/` - Payment processing

---

### 🔧 **common/** - Shared Utilities
**Purpose**: Provides shared utilities, base models, and cross-cutting concerns

**Key Components**:
- `BaseModel` - Common model fields (created_at, updated_at)
- `CurrentUserMiddleware` - Request user context
- `SchedulerService` - Background task scheduling
- Timezone utilities and common permissions

**Services**:
- `SchedulerService` - Task scheduling with threading/Celery
- Common validation and utility functions
- Shared permission classes

---

## Service Layer Architecture

Each domain app implements a **service layer pattern** that separates business logic from models and views:

```python
# Example Service Structure
class TripService:
    @staticmethod
    def create_trip(trip_data):
        """Business logic for trip creation"""
        # Validation, calculations, external API calls
        pass
    
    @staticmethod
    def calculate_flight_time(origin, destination):
        """Flight planning calculations"""
        pass
```

**Benefits**:
- **Separation of Concerns**: Business logic isolated from data and presentation
- **Reusability**: Services can be used across views, management commands, and tests
- **Testability**: Easy to unit test business logic independently
- **Maintainability**: Clear organization of complex operations

## Data Flow & Integration

### 1. **Quote to Trip Workflow**
```
Quote Request → QuoteService.create_quote() → 
Price Calculation → Customer Approval → 
TripService.create_from_quote() → Trip Creation
```

### 2. **Document Generation**
```
Trip Data → DocumentGenerationService → 
Template Processing → Document Creation → 
File Storage → Access Logging
```

### 3. **Payment Processing**
```
Invoice Creation → PaymentProcessorService → 
External Payment API → Transaction Recording → 
Status Updates
```

## Technology Stack

- **Framework**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL (primary), Redis (caching)
- **Authentication**: JWT with token rotation and blacklist
- **Documentation**: drf-yasg for Swagger/OpenAPI
- **Background Tasks**: Celery (optional) or threading
- **External APIs**: Stripe, Square, PayPal for payments

## Security & Permissions

- **JWT Authentication** with access/refresh token rotation
- **Role-Based Access Control (RBAC)** with granular permissions
- **CORS Configuration** for frontend integration
- **HTTPS Enforcement** in production
- **Input Validation** at serializer and service levels

## Testing Strategy

Each app includes comprehensive test coverage:
- **Model Tests**: Data validation and relationships
- **Service Tests**: Business logic validation
- **API Tests**: Endpoint functionality and permissions
- **Integration Tests**: Cross-app workflows

## Deployment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Web Servers   │    │   Database      │
│   (nginx)       │───▶│   (gunicorn)    │───▶│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   Cache/Queue   │
                       │   (Redis)       │
                       └─────────────────┘
```

## Development Guidelines

### Code Organization
- **Models**: Data structure and validation only
- **Services**: Business logic and external integrations
- **Serializers**: API data transformation and validation
- **Views**: HTTP request/response handling
- **URLs**: Clean, RESTful endpoint routing

### Best Practices
- Use service classes for complex business logic
- Implement comprehensive error handling and logging
- Follow Django and DRF conventions
- Write tests for all new features
- Use environment variables for configuration
- Document API endpoints with proper docstrings

This modular architecture transforms a monolithic codebase into a scalable, maintainable system that supports team collaboration and future growth.
