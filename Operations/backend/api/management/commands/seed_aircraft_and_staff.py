from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from django.utils import timezone

from decimal import Decimal
from datetime import datetime
import re

from api.models import (
    Aircraft,
    Contact,
    Staff,
    StaffRole,
    StaffRoleMembership,
)

# -----------------------------
# SOURCE DATA (from your prompt)
# -----------------------------

AIRCRAFT_ROWS = [
    # tail, company, make, model, serial_number, mgtow (lb)
    ("N911KQ", "Secret Squirrel Aerospace LLC", "Kodiak",   "Kodiak 100", "100-0009", "7255"),
    ("N35LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "35A",       "240",      "18300"),
    ("N36LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "36A",       "44",       "18300"),
    ("N30LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "31",        "002",      "18300"),
    ("N60LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "52",       "23500"),
    ("N65LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "243",      "23500"),
    ("N70LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "70",       "23500"),
    ("N80LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "305",      "23500"),
    ("N85LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "244",      "23500"),
    ("N90LJ",  "Worldwide Aircraft Services, Inc.", "Learjet", "60",        "287",      "23500"),
]

PILOT_ROWS = [
    # Name, Nat., DOB, Passport #, Exp., Contact #, Email
    ("Anthony Guglielmetti","US","11/27/1997","534687611","10/27/2025","813-613-1396","AnthonyGuglielmetti@jeticu.com"),
    ("Christopher McGuire","US","11/26/1985","565155697","02/06/2027","813-468-6889","chris.mcguire@jeticu.com"),
    ("Jason Rowe","US","11/20/1982","583027251","11/08/2027","218-343-2005","jrowe@jeticu.com"),
    ("Kurt Veilleux","US","09/17/1983","A35779864","02/08/2034","813-417-6891","kurt@jeticu.com"),
    ("Michael Honeycutt","US","12/18/1969","A03627887","10/13/2032","727-415-9458","mike@jeticu.com"),
    ("John Cannon II","US","05/06/1998","A61105507","02/24/2035","786-879-9393","john.cannon@jeticu.com"),
    ("Patrick Buttermore","US","12/22/1986","A35779865","02/08/2034","813-951-0961","Patrick.Buttermore@jeticu.com"),
    ("Thomas Lacey","US","08/04/1968","A07991093","12/26/2032","727-510-5189","tom@jeticu.com"),
    ("Steven Peterson","US","04/10/1997","A26963982","07/30/2033","845-520-0244","StevePeterson@jeticu.com"),
    ("Tyler Towle","US","04/28/1997","A36095632","10/20/2034","801-824-2782","TylerTowle@jeticu.com"),
    ("Oleg Baumgart","US","01/12/1981","541154548","12/06/2025","575-571-6363","oleg.baumgart@jeticu.com"),
    ("Gary Kelley","US","09/30/1955","561205578","10/11/2027","727-560-0555","puffin@jeticu.com"),
    ("Jack Al-Hussaini","US","11/06/2002","590363317","12/27/2028","704-818-7600","JackAl-Hussaini@jeticu.com"),
]

MEDIC_ROWS = [
    ("Amy Nicole Nilsen","US","05/31/1993","A35874322","05/21/2034","845-421-0106","AMY.NILSEN31@GMAIL.COM"),
    ("Carlos Smith","US","9/10/1972","645442043","04/15/2029","813-454-7837","emnole1995@gmail.com"),
    ("Christopher Izzi","US","12/31/1990","A06603660","06/13/2032","570-856-2730","deltanu239@gmail.com"),
    ("Jacob Samuel Cruz","US","8/10/1995","559629951","04/03/2027","813-340-9103","jcruzmusic16@icloud.com"),
    ("Devin Mormando","US","9/4/1986","A34987989","12/06/2033","352-573-1380","dmormando@elfr.org"),
    ("Jill Butler","US","5/8/1971","678687790","07/04/2032","813-614-4496","jsbutlerrn@gmail.com"),
    ("Eric Castellucci","US","08/10/1953","512319513","01/25/2024","813-417-3210","trilucci@gmail.com"),
    ("Nicholas Mc Sweeney","US","11/6/1990","542911451","04/03/2026","386-588-4005","nickjb_1106@yahoo.com"),
    ("Gary Hurlbut","US","09/26/1968","A03628812","11/20/2032","727-355-3944","AirHurly@gmail.com"),
    ("Harold John Haverty","US","08/23/1961","583528607","05/19/2028","727-504-0451","havertyjohn@yahoo.com"),
    ("James Byrns","US","07/11/1968","A04083672","10/16/2033","727-518-4441","james.byrns68@gmail.com"),
    ("Jamie Lynn Juliano","US","02/18/1983","554218813","07/19/2026","815-641-4906","jamie.juliano7@gmail.com"),
    ("Jared Wayt","US","02/07/1986","565787394","02/26/2028","813-312-4708","jaredw@jeticu.com"),
    ("Jessica May Mone","US","07/22/1978","598263733","06/12/2029","727-599-5138","mjessy0722@gmail.com"),
    ("John David Mulford","US","08/21/1984","A04704947","02/05/2033","813-833-4663","johnmulford@yahoo.com"),
    ("John P. Opyoke","US","7/30/1969","A20507949","05/30/2033","352-263-6925","trinityurgentcare@yahoo.com"),
    ("Jon Inkrott","US","3/17/1972","599921500","07/17/2029","407-516-5579","jon.inkrott@adventhealth.com"),
    ("Justin Andrews","US","10/24/1984","568082572","10/01/2030","239-233-9799","RFinkle5@me.com"),
    ("Kimberly Recinella","US","4/5/1992","673093739","01/23/2032","513-226-1066","ktrecinella@gmail.com"),
    ("Kristin Howell","US","08/17/1984","587818528","09/17/2028","813-361-3009","kristinvictory@gmail.com"),
    ("Kurt Veilleux","US","09/17/1983","520374483","08/03/2024","813-417-6891","kurt@jeticu.com"),
    ("Mary McCarthy","US","11/06/1955","A03492999","02/15/2032","727-641-0085","mary@jeticu.com"),
    ("Michael Abesada","US","01/07/1979","A23420769","10/25/2033","786-447-7153","abesadam@gmail.com"),
    ("Robert Sullivan","US","12/19/1983","572232934","05/24/2027","352-406-2573","bsullivan403@yahoo.com"),
    ("Anthony Marino","US","03/23/1982","674420053","02/10/2032","772-418-0312","antr0323@gmail.com"),
    ("Jefferson Day","US","09/01/1989","A22153633","06/25/2033","352-585-1068","Jeffy_day@yahoo.com"),
    ("Ronald Figueredo","US","7/31/1976","567221355","06/13/2029","610-952-3430","ronaldfigueredo@gmail.com"),
    ("Ronald Wyant","US","09/28/1963","A04483166","09/27/2033","727-639-5126","swyant1@icloud.com"),
    ("Bruce Loeb Jr.","US","01/27/1971","A10316135","11/06/2032","904-338-6447","bnloeb9@gmail.com"),
    ("Thomas Tropeano","US","2/16/1954","549865068","03/13/2027","352-804-9629","tltropeano@yahoo.com"),
    ("Tiffany Bourne","US","03/15/1973","A04483169","09/27/2033","813-260-0343","bourneid73@gmail.com"),
    ("Carla Lynn Sieber","US","07/27/1991","A49128381","11/13/2034","727-424-6886","carlasieber@msn.com"),
    ("Tyson Elledge","US","08/03/1979","A03502556","03/27/2032","352-442-2819","tysonelledge@aol.com"),
    ("Mario Rocha","US","06/02/1970","641826321","03/10/2029","813-215-3277","mario.r.rocha70@gmail.com"),
    ("Jason A. Berger","US","12/10/1990","643816544","09/16/2029","727-512-2959","jberger9359@gmail.com"),
    ("Courtney Hershey","US","05/12/1979","A15958520","03/04/2033","727-519-4714","hersheycourtney@gmail.com"),
]

# Desired role set per cohort
PILOT_ROLE_CODES = ["PIC", "SIC"]
MEDIC_ROLE_CODES = ["RT", "RN", "PARAMEDIC", "MD"]

# Default human-readable names if roles don't exist
ROLE_NAMES_BY_CODE = {
    "PIC": "Pilot in Command",
    "SIC": "Second in Command",
    "RN": "Registered Nurse",
    "PARAMEDIC": "Paramedic",
    "MD": "Physician",
    "RT": "Respiratory Therapist",
}


# -----------------------------
# HELPERS
# -----------------------------

DATE_PATTERNS = ["%m/%d/%Y", "%m/%d/%y", "%m/%-d/%Y", "%m/%-d/%y"]  # macOS strptime may not support %-d; we'll handle manually.

def parse_date(s):
    if not s:
        return None
    s = s.strip()
    # Normalize single-digit months/days to zero-padded mm/dd/yyyy
    # e.g., 9/4/1986 -> 09/04/1986
    parts = re.split(r"[/-]", s)
    if len(parts) == 3:
        mm, dd, yyyy = parts
        if len(mm) == 1: mm = f"0{mm}"
        if len(dd) == 1: dd = f"0{dd}"
        if len(yyyy) == 2:  # assume 20xx for 2-digit years? safer: 19xx for <=30?
            yyyy = "20" + yyyy if int(yyyy) < 50 else "19" + yyyy
        s = f"{mm}/{dd}/{yyyy}"
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def split_name(full_name):
    """
    Split 'First [Middle/Initial/Joint] Last [Suffix]' into first_name, last_name.
    We'll keep everything after the first token as last_name for simplicity,
    but handle common suffixes ("Jr.", "II", "III") gracefully.
    """
    if not full_name:
        return None, None
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], ""
    # Keep suffix attached to last
    suffixes = {"Jr.", "Jr", "Sr.", "Sr", "II", "III", "IV", "V"}
    first = parts[0]
    last = " ".join(parts[1:])
    # compact "Al-Hussaini" etc. untouched
    # nothing more fancy needed for now
    return first, last


def get_or_create_role(code):
    role = StaffRole.objects.filter(code=code).first()
    if role:
        return role
    # Create with default name if missing
    name = ROLE_NAMES_BY_CODE.get(code, code)
    role = StaffRole.objects.create(code=code, name=name)
    return role


def upsert_contact(name, nationality, dob, passport_no, passport_exp, phone, email):
    first_name, last_name = split_name(name)
    # Try to match by email first; fall back to (name + phone)
    contact = None
    if email:
        contact = Contact.objects.filter(email=email.strip()).first()
    if not contact:
        # Try exact name + phone
        contact = Contact.objects.filter(
            first_name=first_name or "",
            last_name=last_name or "",
            phone=(phone or "").strip() or None,
        ).first()

    dob_dt = parse_date(dob)
    pass_exp_dt = parse_date(passport_exp)

    if contact:
        # Update basics if missing
        dirty = False
        if not contact.first_name and first_name:
            contact.first_name = first_name; dirty = True
        if not contact.last_name and last_name:
            contact.last_name = last_name; dirty = True
        if nationality and (contact.nationality != nationality):
            contact.nationality = nationality; dirty = True
        if email and (contact.email != email):
            contact.email = email; dirty = True
        if phone and (contact.phone != phone):
            contact.phone = phone; dirty = True
        if dob_dt and (contact.date_of_birth != dob_dt):
            contact.date_of_birth = dob_dt; dirty = True
        if passport_no and (contact.passport_number != passport_no):
            contact.passport_number = passport_no; dirty = True
        if pass_exp_dt and (contact.passport_expiration_date != pass_exp_dt):
            contact.passport_expiration_date = pass_exp_dt; dirty = True
        if dirty:
            contact.save()
    else:
        contact = Contact.objects.create(
            first_name=first_name or "",
            last_name=last_name or "",
            nationality=nationality or None,
            date_of_birth=dob_dt,
            passport_number=passport_no or None,
            passport_expiration_date=pass_exp_dt,
            phone=phone or None,
            email=email or None,
        )
    return contact


def ensure_staff_for_contact(contact):
    staff = getattr(contact, "staff", None)
    if staff:
        return staff
    return Staff.objects.create(contact=contact, active=True)


def ensure_memberships(staff, role_codes):
    for code in role_codes:
        role = get_or_create_role(code)
        # Do not create duplicates with same open interval (start_on=None, end_on=None)
        exists = StaffRoleMembership.objects.filter(
            staff=staff, role=role, start_on=None, end_on=None
        ).exists()
        if not exists:
            StaffRoleMembership.objects.create(
                staff=staff, role=role, start_on=None, end_on=None
            )


def d(val):
    """Decimal helper for mgtow."""
    if val is None or str(val).strip() == "":
        return None
    return Decimal(str(val))


# -----------------------------
# COMMAND
# -----------------------------

class Command(BaseCommand):
    help = "Seed Aircraft and Staff (Pilots & Medics) into the database."

    def handle(self, *args, **options):
        created_aircraft = updated_aircraft = 0
        created_contacts = updated_contacts = 0
        created_staff = 0
        created_roles = 0
        created_memberships = 0  # (we won't count precisely per-row here; optional)

        # Ensure baseline roles exist (safe if already present)
        for code in set(PILOT_ROLE_CODES + MEDIC_ROLE_CODES):
            if not StaffRole.objects.filter(code=code).exists():
                StaffRole.objects.create(code=code, name=ROLE_NAMES_BY_CODE.get(code, code))
                created_roles += 1

        # --- Aircraft upsert ---
        for tail, company, make, model, serial, mgtow_lb in AIRCRAFT_ROWS:
            mgtow = d(mgtow_lb)  # store the lb number in Decimal (your field is Decimal)
            obj = Aircraft.objects.filter(tail_number=tail).first()
            if obj:
                dirty = False
                if obj.company != company:
                    obj.company = company; dirty = True
                if obj.make != make:
                    obj.make = make; dirty = True
                if obj.model != model:
                    obj.model = model; dirty = True
                if obj.serial_number != serial:
                    obj.serial_number = serial; dirty = True
                if obj.mgtow != mgtow:
                    obj.mgtow = mgtow; dirty = True
                if dirty:
                    obj.save()
                    updated_aircraft += 1
            else:
                Aircraft.objects.create(
                    tail_number=tail,
                    company=company,
                    make=make,
                    model=model,
                    serial_number=serial,
                    mgtow=mgtow,
                )
                created_aircraft += 1

        # --- Pilots ---
        for (name, nat, dob, passport_no, exp, phone, email) in PILOT_ROWS:
            contact_before = Contact.objects.filter(email=email).first()
            contact = upsert_contact(name, nat, dob, passport_no, exp, phone, email)
            if contact_before is None and contact is not None:
                created_contacts += 1
            elif contact_before is not None:
                # we may have updated fields
                updated_contacts += 0  # keep simple; adjust if you want exact diffs

            staff = ensure_staff_for_contact(contact)
            # Before creating, check how many memberships exist to approximate "created_memberships"
            pre_count = StaffRoleMembership.objects.filter(staff=staff).count()
            ensure_memberships(staff, PILOT_ROLE_CODES)
            post_count = StaffRoleMembership.objects.filter(staff=staff).count()
            created_memberships += max(0, post_count - pre_count)

        # --- Medics ---
        for (name, nat, dob, passport_no, exp, phone, email) in MEDIC_ROWS:
            contact_before = Contact.objects.filter(email=email).first()
            contact = upsert_contact(name, nat, dob, passport_no, exp, phone, email)
            if contact_before is None and contact is not None:
                created_contacts += 1
            else:
                updated_contacts += 0

            staff = ensure_staff_for_contact(contact)
            pre_count = StaffRoleMembership.objects.filter(staff=staff).count()
            ensure_memberships(staff, MEDIC_ROLE_CODES)
            post_count = StaffRoleMembership.objects.filter(staff=staff).count()
            created_memberships += max(0, post_count - pre_count)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(
            f"Aircraft: created={created_aircraft}, updated={updated_aircraft}\n"
            f"Contacts: created~={created_contacts}\n"
            f"Staff: ensured (created as needed)\n"
            f"Roles: created={created_roles} (only if missing)\n"
            f"Role memberships created~={created_memberships}"
        )
