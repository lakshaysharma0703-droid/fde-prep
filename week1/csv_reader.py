import csv                      # like: using System.IO;
from pathlib import Path

# Path of the CSV, relative to this script file
csv_path = Path(__file__).parent / "expenses.csv"

totals = {}                     # like: var totals = new Dictionary<string, decimal>();

with open(csv_path, newline="") as f:      # 'with' = C# 'using' block
    reader = csv.DictReader(f)             # each row becomes a dict: row["amount"]
    for row in reader:                     # foreach (var row in reader)
        category = row["category"]
        amount = float(row["amount"])      # decimal.Parse(...)
        totals[category] = totals.get(category, 0) + amount

for category, total in totals.items():     # foreach (var (category, total) in totals)
    print(f"{category}: {total}")          # $"{category}: {total}"