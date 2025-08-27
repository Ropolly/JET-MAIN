# api/management/commands/seed_staff.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from api.models import (
    Staff,
    StaffRole,
    StaffRoleMembership,
    Contact,
    CrewLine,
)

ROLE_CODES = [
    ("PIC", "Pilot in Command"),
    ("SIC", "Second in Command"),
    ("RN", "Registered Nurse"),
    ("PARAMEDIC", "Paramedic"),
    ("RT", "Respiratory Therapist"),
    ("MD", "Physician"),
]


class Command(BaseCommand):
    help = (
        "Seeds StaffRole, backfills Staff for Contacts used on CrewLines, "
        "and (optionally) creates basic StaffRoleMemberships for PIC/SIC."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-memberships",
            action="store_true",
            help="Also create StaffRoleMemberships for PIC/SIC based on CrewLine usage.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        # Ensure roles exist
        created_roles = 0
        for code, name in ROLE_CODES:
            _, was_created = StaffRole.objects.get_or_create(code=code, defaults={"name": name})
            if was_created:
                created_roles += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"StaffRole ensured (created {created_roles}, total {StaffRole.objects.count()})."
            )
        )

        # Collect all Contact IDs referenced by CrewLine (PIC, SIC, and medics)
        contact_ids = set()

        # PIC / SIC via FK fields (use iterator with chunk_size for memory safety)
        for cl in CrewLine.objects.only(
            "primary_in_command_id", "secondary_in_command_id"
        ).iterator(chunk_size=1000):
            if getattr(cl, "primary_in_command_id_id", None):
                contact_ids.add(cl.primary_in_command_id_id)
            if getattr(cl, "secondary_in_command_id_id", None):
                contact_ids.add(cl.secondary_in_command_id_id)

        # Medics via M2M; when using prefetch_related, don't call iterator() without chunk_size
        for cl in CrewLine.objects.prefetch_related("medic_ids"):
            contact_ids.update(cl.medic_ids.values_list("id", flat=True))

        # Backfill Staff rows for those Contacts
        created_staff = 0
        for cid in contact_ids:
            _, was_created = Staff.objects.get_or_create(contact_id=cid, defaults={"active": True})
            if was_created:
                created_staff += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Staff ensured for {len(contact_ids)} contact(s) (created {created_staff})."
            )
        )

        # Optionally add PIC/SIC memberships effective today
        if opts.get("with_memberships"):
            today = timezone.now().date()

            roles = {r.code: r for r in StaffRole.objects.filter(code__in=["PIC", "SIC"])}
            pic = roles.get("PIC")
            sic = roles.get("SIC")

            made = 0

            if pic:
                pic_contact_ids = (
                    CrewLine.objects.exclude(primary_in_command_id__isnull=True)
                    .values_list("primary_in_command_id", flat=True)
                    .distinct()
                )
                for cid in pic_contact_ids:
                    staff = Staff.objects.filter(contact_id=cid).first()
                    if staff and not StaffRoleMembership.objects.filter(
                        staff=staff, role=pic, start_on=today, end_on=None
                    ).exists():
                        StaffRoleMembership.objects.create(
                            staff=staff, role=pic, start_on=today, end_on=None
                        )
                        made += 1

            if sic:
                sic_contact_ids = (
                    CrewLine.objects.exclude(secondary_in_command_id__isnull=True)
                    .values_list("secondary_in_command_id", flat=True)
                    .distinct()
                )
                for cid in sic_contact_ids:
                    staff = Staff.objects.filter(contact_id=cid).first()
                    if staff and not StaffRoleMembership.objects.filter(
                        staff=staff, role=sic, start_on=today, end_on=None
                    ).exists():
                        StaffRoleMembership.objects.create(
                            staff=staff, role=sic, start_on=today, end_on=None
                        )
                        made += 1

            self.stdout.write(self.style.SUCCESS(f"PIC/SIC memberships created today: {made}"))
        else:
            self.stdout.write(
                self.style.WARNING("Skipped memberships (run with --with-memberships to add PIC/SIC).")
            )
