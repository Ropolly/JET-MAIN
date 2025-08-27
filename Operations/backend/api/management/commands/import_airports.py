import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

from api.models import Airport, AirportType  # adjust import path if needed

# Optional timezone lookup
try:
    from timezonefinder import TimezoneFinder
    TF = TimezoneFinder()
except Exception:
    TF = None


def to_decimal(val, places=6):
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        d = Decimal(s)
        return d.quantize(Decimal("0." + "0" * places))
    except (InvalidOperation, ValueError):
        return None


def to_int(val):
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        return int(Decimal(s))
    except (InvalidOperation, ValueError):
        return None


def norm_str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s or None


TYPE_MAP = {
    "large_airport": getattr(AirportType, "LARGE", "large_airport"),
    "medium_airport": getattr(AirportType, "MEDIUM", "medium_airport"),
    "small_airport": getattr(AirportType, "SMALL", "small_airport"),
    "heliport": getattr(AirportType, "SMALL", "small_airport"),
    "seaplane_base": getattr(AirportType, "SMALL", "small_airport"),
    "closed": getattr(AirportType, "SMALL", "small_airport"),
}


def infer_timezone(lat, lon):
    if lat is None or lon is None:
        return "UTC"
    if TF is None:
        return "UTC"
    try:
        tz = TF.timezone_at(lat=float(lat), lng=float(lon))
        return tz or "UTC"
    except Exception:
        return "UTC"


def flush_buffer(buffer, batch_size):
    """Try bulk_create, then fallback to row-by-row on conflicts."""
    created = 0
    skipped = 0
    if not buffer:
        return 0, 0

    try:
        with transaction.atomic():
            Airport.objects.bulk_create(
                buffer, ignore_conflicts=True, batch_size=batch_size
            )
            created += len(buffer)
        return created, skipped
    except IntegrityError:
        pass  # fallback row by row

    for inst in buffer:
        try:
            with transaction.atomic():
                inst.save()
                created += 1
        except IntegrityError:
            skipped += 1
    return created, skipped


class Command(BaseCommand):
    help = "Import airports from a CSV with columns like OurAirports."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to airports.csv")
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing airports matched by ident.",
        )
        parser.add_argument(
            "--batch",
            type=int,
            default=1000,
            help="Bulk create batch size.",
        )

    def handle(self, *args, **opts):
        csv_path = Path(opts["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        update_existing = opts["update"]
        batch_size = opts["batch"]

        created = updated = skipped = 0
        buffer = []

        # preload existing idents for quick lookup
        existing_idents = set(
            Airport.objects.values_list("ident", flat=True)
        )

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                ident = norm_str(row.get("ident"))
                if not ident:
                    skipped += 1
                    continue

                name = norm_str(row.get("name")) or ident
                lat = to_decimal(row.get("latitude_deg"))
                lon = to_decimal(row.get("longitude_deg"))
                elevation = to_int(row.get("elevation_ft"))

                iso_country = norm_str(row.get("iso_country")) or "US"
                iso_region = norm_str(row.get("iso_region"))
                municipality = norm_str(row.get("municipality"))

                icao_code = norm_str(row.get("icao_code"))
                iata_code = norm_str(row.get("iata_code"))
                gps_code = norm_str(row.get("gps_code"))
                local_code = norm_str(row.get("local_code"))

                csv_type = (norm_str(row.get("type")) or "").lower()
                airport_type = TYPE_MAP.get(
                    csv_type, getattr(AirportType, "SMALL", "small_airport")
                )

                tz = infer_timezone(lat, lon)

                defaults = dict(
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    elevation=elevation,
                    iso_country=iso_country,
                    iso_region=iso_region,
                    municipality=municipality,
                    icao_code=icao_code,
                    iata_code=iata_code,
                    local_code=local_code,
                    gps_code=gps_code,
                    airport_type=airport_type,
                    timezone=tz,
                )

                if ident in existing_idents:
                    if update_existing:
                        try:
                            Airport.objects.filter(ident=ident).update(**defaults)
                            updated += 1
                        except IntegrityError:
                            skipped += 1
                    continue
                else:
                    buffer.append(Airport(ident=ident, **defaults))
                    if len(buffer) >= batch_size:
                        c, s = flush_buffer(buffer, batch_size)
                        created += c
                        skipped += s
                        buffer = []

        # flush leftover
        if buffer:
            c, s = flush_buffer(buffer, batch_size)
            created += c
            skipped += s

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: created={created}, updated={updated}, skipped={skipped}"
            )
        )
