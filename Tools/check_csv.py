import sys
from pathlib import Path
import csv

# Supported encodings to try
SUPPORTED_ENCODINGS = ['utf-8', 'windows-1252', 'iso-8859-1']

repo_root = Path(".")
csv_files = [p for p in repo_root.rglob("*.csv")
            if not any(pattern in str(p) for pattern in ['.git', 'node_modules', '__pycache__'])]
error_files = {}
encoding_info = {}

for csv_file in csv_files:
    file_processed = False
    for encoding in SUPPORTED_ENCODINGS:
        try:
            with open(csv_file, "r", encoding=encoding, newline='') as f:
                reader = csv.reader(f)
                row_lengths = set()
                for lineno, row in enumerate(reader, start=1):
                    row_lengths.add(len(row))

                # If we get here, the file was successfully read with this encoding
                encoding_info[csv_file] = encoding
                file_processed = True

                if len(row_lengths) > 1:
                    error_files[csv_file] = f"Inconsistent column count across rows: {sorted(row_lengths)} (encoding: {encoding})"
                break
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except Exception as e:
            # Other errors (like CSV parsing issues) - try next encoding
            continue

    if not file_processed:
        error_files[csv_file] = f"Could not read file with any supported encoding: {SUPPORTED_ENCODINGS}"

if error_files:
    print("Found CSV files incompatible with RFC4180 section 2:\n")
    for f, err in error_files.items():
        print(f"  {f}: {err}")
    sys.exit(1)
else:
    print("All CSV files appear to be RFC4180 section 2 compatible!")
    print("\nEncoding information:")
    for f, encoding in encoding_info.items():
        print(f"  {f}: {encoding}")

