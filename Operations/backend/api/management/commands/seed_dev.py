# api/management/commands/seed_dev.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, connection
from decimal import Decimal
from datetime import timedelta, datetime
from django.utils import timezone
from uuid import UUID

from api.models import (
    Permission, Role, Department, UserProfile, Contact, FBO, Ground, Airport,
    Document, Aircraft, Transaction, Agreement, Patient, Quote, Passenger,
    CrewLine, Trip, TripLine
)

def aware(dt_str: str):
    dt = datetime.fromisoformat(dt_str)
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt

class Command(BaseCommand):
    help = "Seed development/test data"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.NOTICE("Seeding data..."))

            # --- Base users for created_by/modified_by ---
            admin_user, _ = User.objects.get_or_create(
                username="admin",
                defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
            )
            if not admin_user.has_usable_password():
                admin_user.set_password("admin123")
                admin_user.save()

            alice_user, _ = User.objects.get_or_create(
                username="alice",
                defaults={"email": "alice@example.com", "is_staff": True}
            )
            if not alice_user.has_usable_password():
                alice_user.set_password("password123")
                alice_user.save()

            bob_user, _ = User.objects.get_or_create(
                username="bob",
                defaults={"email": "bob@example.com"}
            )
            if not bob_user.has_usable_password():
                bob_user.set_password("password123")
                bob_user.save()

            # --- Your explicit auth_user id=7 + exact hash/timestamps ---
            target_user_id = 7
            password_hash = "pbkdf2_sha256$870000$FXqSBkZnJCTre722mo1IwH$feY/56s+7Ry8EnAEmrNRFZdw0q7jZZ6KmjM6jly+R2s="
            last_login_str = "2025-08-16 16:34:56.213251"
            date_joined_str = "2025-08-16 15:54:58.108485"

            u7, created = User.objects.get_or_create(
                id=target_user_id,
                defaults=dict(
                    username="chaimkitchner",
                    email="ck@cekitch.com",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                    password=password_hash,
                    last_login=aware(last_login_str),
                    date_joined=aware(date_joined_str),
                ),
            )
            if not created:
                u7.username = "chaimkitchner"
                u7.email = "ck@cekitch.com"
                u7.is_superuser = True
                u7.is_staff = True
                u7.is_active = True
                u7.password = password_hash
                u7.save(update_fields=["username", "email", "is_superuser", "is_staff", "is_active", "password"])
                User.objects.filter(pk=u7.pk).update(
                    last_login=aware(last_login_str),
                    date_joined=aware(date_joined_str),
                )

            # bump sequence in Postgres so future inserts don't collide with id=7
            if connection.vendor == "postgresql":
                with connection.cursor() as cur:
                    cur.execute(
                        "SELECT setval(pg_get_serial_sequence('auth_user','id'), "
                        "(SELECT GREATEST(COALESCE(MAX(id), 1), 1) FROM auth_user))"
                    )

            # --- Matching api_userprofile record (UUID + timestamps you provided) ---
            profile_id = UUID("26e9897c-9ffe-427d-beaa-e1c6e8978f19")
            created_on_str = "2025-08-16 16:46:57.983721"
            modified_on_str = "2025-08-21 06:52:22.459238"

            up_defaults = dict(
                user=u7,
                first_name="Chaim",
                last_name="Kitchner",
                email="ck@cekitch.com",
                status="active",
                lock=False,
                created_by=u7,
                modified_by=u7,
            )
            up, up_created = UserProfile.objects.get_or_create(id=profile_id, defaults=up_defaults)
            if not up_created:
                up.user = u7
                up.first_name = "Chaim"
                up.last_name = "Kitchner"
                up.email = "ck@cekitch.com"
                up.status = "active"
                up.lock = False
                up.created_by = u7
                up.modified_by = u7
                up.save()
            UserProfile.objects.filter(pk=profile_id).update(
                created_on=aware(created_on_str),
                modified_on=aware(modified_on_str),
            )

            # --- Permissions / Roles / Departments ---
            p_view, _ = Permission.objects.get_or_create(
                name="view_quotes",
                defaults={"description": "Can view quotes", "created_by": admin_user, "modified_by": admin_user},
            )
            p_edit, _ = Permission.objects.get_or_create(
                name="edit_quotes",
                defaults={"description": "Can edit quotes", "created_by": admin_user, "modified_by": admin_user},
            )
            p_trips, _ = Permission.objects.get_or_create(
                name="manage_trips",
                defaults={"description": "Can manage trips", "created_by": admin_user, "modified_by": admin_user},
            )

            role_admin, _ = Role.objects.get_or_create(
                name="Admin",
                defaults={"description": "Admin role", "created_by": admin_user, "modified_by": admin_user},
            )
            role_admin.permissions.set([p_view, p_edit, p_trips])

            role_ops, _ = Role.objects.get_or_create(
                name="Dispatcher",
                defaults={"description": "Operations/Dispatcher", "created_by": admin_user, "modified_by": admin_user},
            )
            role_ops.permissions.set([p_view, p_trips])

            dept_ops, _ = Department.objects.get_or_create(
                name="Operations",
                defaults={"description": "Ops department", "created_by": admin_user, "modified_by": admin_user},
            )
            dept_med, _ = Department.objects.get_or_create(
                name="Medical",
                defaults={"description": "Medical department", "created_by": admin_user, "modified_by": admin_user},
            )
            dept_ops.permission_ids.set([p_view, p_trips, p_edit])
            dept_med.permission_ids.set([p_view])

            # hook M2Ms for user profiles
            up.roles.set([role_admin])
            up.departments.set([dept_ops])
            up.department_ids.set([dept_ops])

            # --- Contacts (pilots/medic/customer) ---
            pilot1, _ = Contact.objects.get_or_create(
                first_name="Pat", last_name="Pilot",
                defaults={"email": "pat.pilot@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pilot2, _ = Contact.objects.get_or_create(
                first_name="Sam", last_name="Second",
                defaults={"email": "sam.second@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            medic1, _ = Contact.objects.get_or_create(
                first_name="Rory", last_name="RN",
                defaults={"email": "rory.rn@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            customer, _ = Contact.objects.get_or_create(
                business_name="Oceanic Cruises",
                defaults={"email": "ops@oceanic.example.com", "created_by": admin_user, "modified_by": admin_user},
            )

            # --- FBO / Ground / Airports ---
            fbo_jfk, _ = FBO.objects.get_or_create(
                name="Signature JFK",
                defaults={"city": "New York", "state": "NY", "created_by": admin_user, "modified_by": admin_user},
            )
            fbo_jfk.contacts.set([pilot1])

            ground_lax, _ = Ground.objects.get_or_create(
                name="LAX Limo",
                defaults={"city": "Los Angeles", "state": "CA", "created_by": admin_user, "modified_by": admin_user},
            )
            ground_lax.contacts.set([customer])

            jfk, _ = Airport.objects.get_or_create(
                icao_code="KJFK",
                defaults=dict(
                    iata_code="JFK", name="John F. Kennedy International", city="New York",
                    state="NY", country="USA", elevation=13,
                    latitude=Decimal("40.641311"), longitude=Decimal("-73.778139"),
                    timezone="America/New_York", created_by=admin_user, modified_by=admin_user
                ),
            )
            lax, _ = Airport.objects.get_or_create(
                icao_code="KLAX",
                defaults=dict(
                    iata_code="LAX", name="Los Angeles International", city="Los Angeles",
                    state="CA", country="USA", elevation=125,
                    latitude=Decimal("33.941589"), longitude=Decimal("-118.408530"),
                    timezone="America/Los_Angeles", created_by=admin_user, modified_by=admin_user
                ),
            )
            jfk.fbos.add(fbo_jfk)
            lax.grounds.add(ground_lax)

            # --- Aircraft ---
            aircraft, _ = Aircraft.objects.get_or_create(
                tail_number="N123AB",
                defaults=dict(
                    company="Airmed Partners", mgtow=Decimal("21500.00"),
                    make="Learjet", model="35A", serial_number="LJ35-0001",
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            # --- Documents & Agreements ---
            pdf_bytes = b"%PDF-1.4 test\n%%EOF"
            doc_quote, _ = Document.objects.get_or_create(filename="quote.pdf", defaults={"content": pdf_bytes})
            doc_agree, _ = Document.objects.get_or_create(filename="agreement.pdf", defaults={"content": pdf_bytes})
            doc_passport, _ = Document.objects.get_or_create(filename="passport.jpg", defaults={"content": b'\x00\x01TEST'})

            agreement_payment, _ = Agreement.objects.get_or_create(
                destination_email="billing@oceanic.example.com",
                defaults={"document_unsigned": doc_agree, "status": "created",
                          "created_by": admin_user, "modified_by": admin_user},
            )
            agreement_consent, _ = Agreement.objects.get_or_create(
                destination_email="consent@oceanic.example.com",
                defaults={"document_unsigned": doc_agree, "status": "created",
                          "created_by": admin_user, "modified_by": admin_user},
            )

            # --- Patient / Passengers ---
            patient_contact, _ = Contact.objects.get_or_create(
                first_name="Jamie", last_name="Doe",
                defaults={"email": "jamie@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            patient, _ = Patient.objects.get_or_create(
                info=patient_contact,
                defaults=dict(
                    bed_at_origin=True, bed_at_destination=False,
                    date_of_birth=timezone.now().date().replace(year=1988),
                    nationality="USA", passport_number="X1234567",
                    passport_expiration_date=timezone.now().date().replace(year=2032),
                    passport_document=doc_passport, status="pending",
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            pax_contact1, _ = Contact.objects.get_or_create(
                first_name="Alex", last_name="Doe",
                defaults={"email": "alex@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pax1, _ = Passenger.objects.get_or_create(
                info=pax_contact1,
                defaults=dict(
                    nationality="USA", passport_number="PAX001",
                    passport_expiration_date=timezone.now().date().replace(year=2030),
                    contact_number="+1-555-0110", passport_document=doc_passport,
                    created_by=admin_user, modified_by=admin_user
                ),
            )

            pax_contact2, _ = Contact.objects.get_or_create(
                first_name="Taylor", last_name="Smith",
                defaults={"email": "taylor@example.com", "created_by": admin_user, "modified_by": admin_user},
            )
            pax2, _ = Passenger.objects.get_or_create(
                info=pax_contact2,
                defaults=dict(
                    nationality="USA", passport_number="PAX002",
                    passport_expiration_date=timezone.now().date().replace(year=2031),
                    contact_number="+1-555-0111", passport_document=doc_passport,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            pax1.passenger_ids.add(pax2)

            # --- Crew Line ---
            crew, _ = CrewLine.objects.get_or_create(
                primary_in_command=pilot1,
                secondary_in_command=pilot2,
                defaults={"created_by": admin_user, "modified_by": admin_user},
            )
            crew.medic_ids.set([medic1])

            # --- Quote ---
            quote, _ = Quote.objects.get_or_create(
                contact=customer, pickup_airport=jfk, dropoff_airport=lax,
                defaults=dict(
                    quoted_amount=Decimal("45999.00"),
                    aircraft_type="35",
                    estimated_flight_time=timedelta(hours=5, minutes=30),
                    includes_grounds=True, inquiry_date=timezone.now(),
                    medical_team="RN/Paramedic", patient=patient,
                    status="pending", number_of_stops=1,
                    quote_pdf=doc_quote, quote_pdf_status="created",
                    quote_pdf_email="quotes@airmed.example.com",
                    payment_agreement=agreement_payment,
                    consent_for_transport=agreement_consent,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            quote.documents.set([doc_quote])

            # --- Transaction ---
            txn, _ = Transaction.objects.get_or_create(
                email="payer@oceanic.example.com",
                amount=Decimal("10000.00"),
                payment_method="credit_card",
                defaults=dict(
                    payment_status="completed",
                    payment_date=timezone.now(),
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            quote.transactions.add(txn)

            # --- Trip + legs ---
            trip, _ = Trip.objects.get_or_create(
                trip_number="TRIP-0001",
                defaults=dict(
                    email_chain=[], quote=quote, type="medical", patient=patient,
                    estimated_departure_time=timezone.now() + timedelta(days=3, hours=2),
                    post_flight_duty_time=timedelta(hours=2),
                    pre_flight_duty_time=timedelta(hours=1),
                    aircraft=aircraft,
                    internal_itinerary=doc_quote,
                    customer_itinerary=doc_quote,
                    created_by=admin_user, modified_by=admin_user
                ),
            )
            trip.passengers.set([pax1, pax2])

            dep_utc = timezone.now() + timedelta(days=3, hours=2)
            arr_utc = dep_utc + timedelta(hours=6)
            TripLine.objects.get_or_create(
                trip=trip, origin_airport=jfk, destination_airport=lax,
                departure_time_local=dep_utc, departure_time_utc=dep_utc,
                arrival_time_local=arr_utc, arrival_time_utc=arr_utc,
                defaults=dict(
                    crew_line=crew, distance=Decimal("2475.50"),
                    flight_time=timedelta(hours=6), ground_time=timedelta(minutes=45),
                    passenger_leg=True, created_by=admin_user, modified_by=admin_user
                ),
            )

            dep2 = arr_utc + timedelta(hours=2)
            arr2 = dep2 + timedelta(hours=5, minutes=45)
            TripLine.objects.get_or_create(
                trip=trip, origin_airport=lax, destination_airport=jfk,
                departure_time_local=dep2, departure_time_utc=dep2,
                arrival_time_local=arr2, arrival_time_utc=arr2,
                defaults=dict(
                    crew_line=crew, distance=Decimal("2475.50"),
                    flight_time=timedelta(hours=5, minutes=45), ground_time=timedelta(minutes=30),
                    passenger_leg=True, created_by=admin_user, modified_by=admin_user
                ),
            )

            self.stdout.write(self.style.SUCCESS("✅ Seed complete."))
            self.stdout.write(self.style.SUCCESS("Users: admin/admin123; alice/bob with password123"))
            self.stdout.write(self.style.SUCCESS("Custom user id=7: chaimkitchner (pre-hashed)"))
