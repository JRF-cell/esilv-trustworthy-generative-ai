
import csv

files = [
    "traces-A-new.csv",
    "traces-B.csv",
    "traces-C.csv",
    "traces-D.csv",
    "traces-E.csv",
]

all_rows = []
columns = None

for filename in files:
    with open(filename, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        if columns is None:
            columns = reader.fieldnames
        elif reader.fieldnames != columns:
            raise ValueError(f"Colonnes incompatibles : {filename}")

        rows = list(reader)
        all_rows.extend(rows)
        print(f"{filename}: {len(rows)} traces")

with open("traces-td1.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\nFusion terminee : {len(all_rows)} traces")
