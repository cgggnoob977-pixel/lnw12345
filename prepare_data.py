import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "library_book_loans_dirty_150.csv"
OUTPUT = ROOT / "assets" / "library_book_loans_prepared_149.csv"


def main():
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as source_file:
        reader = csv.DictReader(source_file)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {SOURCE}")
        rows = list(reader)
        headers = reader.fieldnames

    loan_id = "รหัสการยืม"
    if loan_id not in headers:
        raise ValueError(f"Required column is missing: {loan_id}")

    seen = set()
    prepared = []
    duplicate_count = 0
    for row in rows:
        cleaned = {key: (value or "").strip() for key, value in row.items()}
        key = cleaned[loan_id]
        if key and key in seen:
            duplicate_count += 1
            continue
        if key:
            seen.add(key)
        prepared.append(cleaned)

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(prepared)

    print(f"Source rows: {len(rows)}")
    print(f"Duplicate rows excluded: {duplicate_count}")
    print(f"Prepared rows: {len(prepared)}")
    print(f"Prepared CSV: {OUTPUT}")


if __name__ == "__main__":
    main()
