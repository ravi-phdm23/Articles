import pandas as pd
import json
import sys


def parse_excel(path: str):
    df = pd.read_excel(path)
    entries = []
    group_cols = ['Requirement', 'TestDescription']
    grouped = df.groupby(group_cols)
    for (req, desc), group in grouped:
        lines = []
        for i, (_, row) in enumerate(group.iterrows(), 1):
            step = str(row['TestStep']).strip()
            data = str(row['TestData']).strip()
            expected = str(row['ExpectedResults']).strip()
            line = f"Step {i}: {step}"
            if data and data != 'nan':
                line += f"\nTest Data: {data}"
            if expected and expected != 'nan':
                line += f"\nExpected Result: {expected}"
            lines.append(line)
        output_text = "\n".join(lines)
        entries.append({
            "instruction": f"{req} - {desc}",
            "input": "",
            "output": output_text
        })
    return entries


def main():
    if len(sys.argv) != 3:
        print("Usage: python prepare_excel_alpaca.py <input_xlsx> <output_json>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    entries = parse_excel(inp)
    with open(outp, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(entries)} entries to {outp}")


if __name__ == '__main__':
    main()
