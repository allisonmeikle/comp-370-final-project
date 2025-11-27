import csv
from datetime import datetime

IN_PATH = "articles_final.csv"          # input
OUT_PATH = "articles_final_fixed.csv"  # output

def convert_date(s: str) -> str:
    if not s:
        return s
    raw = s.strip()

    # Already ISO / starts with year → leave alone
    if raw[0].isdigit():
        return raw

    # Normalize weird "17:16pm" style:
    lower = raw.lower()
    if lower.endswith("am") or lower.endswith("pm"):
        # strip trailing am/pm but keep the time part
        raw = raw[:-2].strip()

    # Try formats WITH time
    time_formats = [
        "%b %d, %Y %H:%M",    # Nov 18, 2025 17:16
        "%b %d %Y %H:%M",     # Nov 18 2025 17:16
        "%B %d, %Y %H:%M",    # November 18, 2025 17:16
        "%B %d %Y %H:%M",     # November 18 2025 17:16
        "%b %d, %Y %I:%M%p",  # Nov 18, 2025 5:16pm
        "%B %d, %Y %I:%M%p",  # November 18, 2025 5:16pm
    ]

    date_only_formats = [
        "%b %d, %Y",          # Nov 18, 2025
        "%b %d %Y",           # Nov 18 2025
        "%b %d",              # Nov 18  (assume 2025)
        "%B %d, %Y",          # November 18, 2025
        "%B %d %Y",           # November 18 2025
        "%B %d",              # November 18 (assume 2025)
    ]

    dt = None

    # First try with time
    for fmt in time_formats:
        try:
            dt = datetime.strptime(raw, fmt)
            break
        except ValueError:
            continue

    # If that failed, try date-only and default to noon
    if dt is None:
        for fmt in date_only_formats:
            try:
                dt = datetime.strptime(raw, fmt)
                # no time → default noon
                dt = dt.replace(hour=12, minute=0, second=0)
                break
            except ValueError:
                continue

    if dt is None:
        # Couldn't parse → leave unchanged so we don't corrupt data
        return s

    # If year defaulted to 1900, assume 2025
    if dt.year == 1900:
        dt = dt.replace(year=2025)

    # Final format: 2025-11-18T17:16:00-05:00
    return dt.strftime("%Y-%m-%dT%H:%M:%S-05:00")


with open(IN_PATH, newline="") as f_in, open(OUT_PATH, "w", newline="") as f_out:
    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        if "date" in row and row["date"]:
            row["date"] = convert_date(row["date"])
        writer.writerow(row)
