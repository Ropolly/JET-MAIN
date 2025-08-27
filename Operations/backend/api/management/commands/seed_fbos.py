import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import FBO, Airport  # adjust import path if different


HEADERS = {
    "icao": ("ID", "ICAO", "Airport", "Airport ID"),
    "name": ("FBO", "Name"),
    "phone": ("PHONE", "Phone"),
    "phone2": ("PHONE2", "Phone2", "Alt Phone"),
    "email": ("Email", "E-mail"),
    "notes": ("FBO NOTES", "Notes"),
}


def pick(row, keys):
    """Return the first non-empty trimmed value from row for any of the provided keys."""
    for k in keys:
        if k in row and row[k] is not None:
            v = str(row[k]).strip()
            if v != "":
                return v
    return ""


class Command(BaseCommand):
    help = "Seed FBO records from a CSV and link them to Airports by ICAO code."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file.")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report without writing any changes.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing FBO phone/email/notes if new data present.",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        dry_run = opts["dry_run"]
        do_update = opts["update"]

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        created_fbos = 0
        linked_pairs = 0
        updated_fbos = 0
        skipped_rows = 0
        missing_airports = 0

        # Read CSV with BOM tolerance
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            # Normalize header keys once (DictReader preserves original)
            # We'll still use the HEADERS map via pick()

            for i, row in enumerate(reader, start=2):  # start=2 accounts for header row = line 1
                icao = pick(row, HEADERS["icao"]).upper()
                name = pick(row, HEADERS["name"])
                phone = pick(row, HEADERS["phone"])
                phone2 = pick(row, HEADERS["phone2"])
                email = pick(row, HEADERS["email"])
                notes = pick(row, HEADERS["notes"])

                if not icao or not name:
                    skipped_rows += 1
                    self.stdout.write(self.style.WARNING(
                        f"[line {i}] Skipped: missing required ICAO and/or FBO name."
                    ))
                    continue

                airport = Airport.objects.filter(icao_code__iexact=icao).first()
                if not airport:
                    missing_airports += 1
                    self.stdout.write(self.style.WARNING(
                        f"[line {i}] No Airport found for ICAO '{icao}'. Row skipped."
                    ))
                    continue

                # Try to find an existing FBO by name (+email/phone if available) to avoid global name collisions
                fbo_qs = FBO.objects.filter(name__iexact=name)
                if email:
                    fbo_qs = fbo_qs.filter(email__iexact=email) | fbo_qs
                if phone:
                    fbo_qs = fbo_qs.filter(phone__iexact=phone) | fbo_qs

                fbo = fbo_qs.distinct().first()

                if fbo is None:
                    # Create new FBO
                    fbo = FBO(
                        name=name,
                        phone=phone or None,
                        phone_secondary=phone2 or None,
                        email=email or None,
                        notes=notes or None,
                    )
                    if not dry_run:
                        fbo.save()
                    created_fbos += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"[line {i}] Created FBO '{name}'."
                    ))
                else:
                    # Optionally update existing with any new info provided
                    if do_update:
                        changed = False
                        if phone and fbo.phone != phone:
                            fbo.phone = phone
                            changed = True
                        if phone2 and fbo.phone_secondary != phone2:
                            fbo.phone_secondary = phone2
                            changed = True
                        if email and (fbo.email or "").lower() != email.lower():
                            fbo.email = email
                            changed = True
                        if notes and (fbo.notes or "").strip() != notes:
                            fbo.notes = notes
                            changed = True
                        if changed and not dry_run:
                            fbo.save()
                            updated_fbos += 1
                            self.stdout.write(self.style.SUCCESS(
                                f"[line {i}] Updated FBO '{name}'."
                            ))

                # Link to Airport via M2M (Airport ↔ FBO)
                if not dry_run:
                    airport.fbos.add(fbo)
                linked_pairs += 1

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN: no changes were written."))

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created FBOs: {created_fbos}, Updated: {updated_fbos}, "
            f"Linked (Airport↔FBO): {linked_pairs}, Skipped rows: {skipped_rows}, "
            f"Missing airports: {missing_airports}"
        ))
