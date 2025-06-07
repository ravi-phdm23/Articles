import csv
import json
import sys
from typing import List, Dict


def parse_dataset(csv_path: str) -> List[Dict[str, str]]:
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    entries = []
    current_instruction = None
    output_lines: List[str] = []

    for row in rows[1:]:  # skip header
        # Ensure row has at least 2 columns
        if len(row) < 2:
            continue
        col0, col1 = row[0].strip(), row[1].strip()

        if col0 and col1:
            # New instruction encountered
            if current_instruction:
                entries.append({
                    "instruction": current_instruction,
                    "input": "",
                    "output": "\n".join(output_lines).strip()
                })
            current_instruction = col0
            output_lines = [col1]
        elif col0 and not col1:
            # Section header; finalize any in-progress entry
            if current_instruction:
                entries.append({
                    "instruction": current_instruction,
                    "input": "",
                    "output": "\n".join(output_lines).strip()
                })
            current_instruction = None
            output_lines = []
        elif not col0 and col1:
            if current_instruction:
                output_lines.append(col1)
        else:
            # Blank row
            continue

    if current_instruction:
        entries.append({
            "instruction": current_instruction,
            "input": "",
            "output": "\n".join(output_lines).strip()
        })

    return entries


def main():
    if len(sys.argv) != 3:
        print("Usage: python prepare_alpaca_dataset.py <input_csv> <output_json>")
        sys.exit(1)

    input_csv, output_json = sys.argv[1], sys.argv[2]
    entries = parse_dataset(input_csv)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(entries)} entries to {output_json}")


if __name__ == "__main__":
    main()
