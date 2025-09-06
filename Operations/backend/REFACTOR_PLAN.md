# Django Project Refactoring Plan

## Current Structure Issues
- Monolithic `api/` app with 22k+ lines in models.py
- All business logic mixed in models and views
- Utils scattered without clear organization
- No clear separation of concerns

## Proposed New Structure

```
backend/
├── manage.py
├── requirements.txt
├── backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                          # Authentication & User Management
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # UserProfile, Role, Permission, Department
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── permission_service.py
│   └── tests.py
├── contacts/                       # Contact Management
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Contact, FBO, Ground
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── contact_service.py      # Move from api/contact_service.py
│   └── tests.py
├── airports/                       # Airport Data & Scrapers
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Airport, AirportType
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── airport_service.py
│   │   └── weather_scraper.py      # From utils/webscraping/
│   └── tests.py
├── aircraft/                       # Aircraft & Maintenance
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Aircraft
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── maintenance_service.py
│   └── tests.py
├── operations/                     # Core Operations
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Trip, TripLine, CrewLine, Passenger, Patient, Quote, TripEvent
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── trip_service.py
│   │   ├── quote_service.py
│   │   └── crew_service.py
│   └── tests.py
├── documents/                      # Document Storage & Generation
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Document, Agreement
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py
│   │   └── generation_service.py   # Integrate with utils/docgen/
│   └── tests.py
├── finance/                        # Financial Operations
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                   # Transaction
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── payment_service.py      # From utils/paymentprocess/
│   └── tests.py
├── content/                        # CMS-like content (merge index/)
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── common/                         # Shared utilities
│   ├── __init__.py
│   ├── models.py                   # BaseModel, Modification, Comment
│   ├── permissions.py              # Move from api/permissions.py
│   ├── middleware.py               # Move from api/middleware.py
│   ├── timezone_utils.py           # Move from api/timezone_utils.py
│   └── utils.py                    # Move from api/utils.py
└── utils/                          # Global utilities
    ├── __init__.py
    ├── docgen/                     # Keep document generation utilities
    │   └── ...
    └── schedulers/                 # Keep async task utilities
        └── ...
```

## Migration Strategy

### Phase 1: Create New Apps
1. Create new Django apps with proper structure
2. Move models to appropriate apps
3. Update foreign key references
4. Create services modules

### Phase 2: Move Business Logic
1. Extract business logic from models to services
2. Update views to use services
3. Create proper serializers for each app

### Phase 3: Update Configuration
1. Update INSTALLED_APPS in settings
2. Create new URL patterns
3. Update admin configurations

### Phase 4: Testing & Cleanup
1. Convert test scripts to proper Django tests
2. Remove old api/ app
3. Update documentation

## Benefits
- **Modularity**: Each app has a single responsibility
- **Scalability**: Easy to add new features within domain boundaries
- **Maintainability**: Clear separation of concerns
- **Testing**: Isolated testing per domain
- **Team Development**: Multiple developers can work on different apps
