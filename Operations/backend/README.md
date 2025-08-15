# JET ICU Operations Backend

This is the Django backend for the JET ICU Operations system, a management platform for a jet ambulance company.

## Project Structure

The backend is built with Django and Django REST Framework, following a standard structure:

- `api/` - Main application containing models, views, serializers
- `backend/` - Project configuration

## Models

The system includes the following key models:

- **Base Models**: Permission, Role, Department, UserProfile
- **Contact Management**: Contact, FBO, Ground
- **Location Management**: Airport
- **Equipment**: Aircraft
- **Document Management**: Document
- **Financial**: Transaction
- **Agreements**: Agreement
- **Patient Management**: Patient, Passenger
- **Operations**: Quote, Trip, TripLine, CrewLine
- **Change Tracking**: Modification

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

The API is available at `/api/` and includes the following endpoints:

- `/api/permissions/` - Permission management
- `/api/roles/` - Role management
- `/api/departments/` - Department management
- `/api/users/` - User management
- `/api/contacts/` - Contact management
- `/api/fbos/` - FBO management
- `/api/grounds/` - Ground transportation management
- `/api/airports/` - Airport management
- `/api/documents/` - Document management
- `/api/aircraft/` - Aircraft management
- `/api/transactions/` - Transaction management
- `/api/agreements/` - Agreement management
- `/api/patients/` - Patient management
- `/api/quotes/` - Quote management
- `/api/passengers/` - Passenger management
- `/api/crew-lines/` - Crew line management
- `/api/trips/` - Trip management
- `/api/trip-lines/` - Trip line management
- `/api/modifications/` - Change tracking

## Authentication

Authentication is handled via token authentication:

- To obtain a token: `POST /api-token-auth/` with username and password
- Include the token in the Authorization header: `Authorization: Token <your-token>`

## Business Process Flow

1. Quote creation from initial contact
2. Document generation and agreement signing
3. Payment processing
4. Trip creation with itinerary
5. Automatic time calculations for trip legs
