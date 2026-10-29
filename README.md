# Sales Report Generator

Turns your monthly sales CSV files into a clean summary report.
Put the files in a folder, run one command, and get revenue per month and your top products.
Bad rows and unreadable files are skipped and listed in the report instead of crashing the tool.

## Example output

```text
=== Sales Report ===

Revenue per month:
  jan    117.00€
  feb    112.50€
  mar    131.00€

Top products:
  1. Apple     185.00€
  2. Book       72.00€
  3. Banana     65.00€
  4. Pen        38.50€

Skipped rows: 1
  mar.csv, row 6

Grand total: 360.50€
```

## Requirements

Python 3 (no extra packages needed).

## How to run

1. Download `sales_report.py` and the `sample_data` folder.
2. In a terminal, in that folder, run:

```powershell
py sales_report.py
```

To use your own files and choose the report name:

```powershell
py sales_report.py --data-dir "path\to\your\folder" --output my_report.txt
```

## What you get

- `report.txt` (or the name you chose): the summary report
- `results_all.csv`: every product's revenue per month, for use in other reports
- `sales_report.log`: detailed log of what happened

## Input format

Each CSV needs the header `product,price,quantity`, for example:

```csv
product,price,quantity
Pen,3,2
Book,4,10
kiwi,abc,15
```

File names are used as month names (`jan.csv`, `feb.csv`, ...).

## Handling bad data

- **Bad row** (like `kiwi,abc,15` above): skipped and listed in the report. The rest of the file is still counted.
- **Wrong header** (a missing or misspelled column): the whole file is skipped and listed under "Skipped files". Other files are still processed.
- **No usable data at all:** no report is written, and the tool exits with an error.

## Limitations

Products with zero sales don't appear in "Top products".
