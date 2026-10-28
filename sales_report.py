import csv
from pathlib import Path
import argparse
import logging

SCRIPT_DIR = Path(__file__).parent

#Argparese
parser = argparse.ArgumentParser(description="Create a sales report from monthly CSV files.")
parser.add_argument("--data-dir", default=None, help="Folder containing the CSV files.")
parser.add_argument("-o", "--output", default=None, help="Where the report gets written")
args = parser.parse_args()

file_handler = logging.FileHandler(SCRIPT_DIR / "sales_report.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.DEBUG,
    format= "%(asctime)s %(levelname)s %(message)s",
    handlers=[file_handler, console],
)

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]

def month_key(path):
    name = path.stem.lower()
    # Unknown file names go to the end, sorted alphabetically
    return (MONTHS.index(name) if name in MONTHS else len(MONTHS), name)


def read_sales(path):
    good_rows = []
    skipped_rows = []

    with open(path, mode='r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row_nr, row in enumerate(csv_reader, start=2):
            try:
                price = float(row['price'])
                quantity = int(row['quantity'])
            except ValueError:
                logging.warning("%s: row %s skipped (invalid data)", Path(path).name, row_nr)
                skipped_rows.append((Path(path).name, row_nr))
                continue

            good_rows.append((row['product'], price, quantity))

    return good_rows, skipped_rows


def main():
    all_results = []
    all_skipped = []
    month_totals = {}
    product_totals = {}
    data_dir = Path(args.data_dir) if args.data_dir else SCRIPT_DIR/ "sample_data"
    output_path = Path(args.output) if args.output else SCRIPT_DIR / "report.txt"
    csv_files = sorted(data_dir.glob("*.csv"), key=month_key)
    if not csv_files:
        print(f"No CSV files found in: {data_dir}")
        raise SystemExit(1)

    for path in csv_files:
        month = path.stem
        good_rows, skipped_rows = read_sales(path)
        all_skipped.extend(skipped_rows)

        file_total = 0
        for product, price, quantity in good_rows:
            revenue = price * quantity

            if quantity > 0:
                file_total += revenue
                product_totals[product] = product_totals.get(product, 0) + revenue
                logging.debug("%s: %.2f x %s = %.2f", product, price, quantity, revenue)
            else:
                logging.debug("%s: no sales", product)

            all_results.append([month, product, revenue])

        month_totals[month] = file_total
        logging.info("Total revenue %s: %.2f€", month, file_total)

    # --- Aggregation ---
    top_products = sorted(product_totals.items(), key=lambda item: item[1], reverse=True)
    grand_total = sum(month_totals.values())

    # --- Build report ---
    month_width = max((len(m) for m in month_totals), default=0)
    product_width = max((len(p) for p in product_totals), default=0)

    lines = ["=== Sales Report ===", "", "Revenue per month:"]
    for month, total in month_totals.items():
        lines.append(f"  {month:<{month_width}}  {total:>8.2f}€")

    lines += ["", "Top products:"]
    for rank, (product, total) in enumerate(top_products, start=1):
        lines.append(f"  {rank}. {product:<{product_width}}  {total:>8.2f}€")

    lines += ["", f"Skipped rows: {len(all_skipped)}"]
    for file_name, row_nr in all_skipped:
        lines.append(f"  {file_name}, row {row_nr}")

    lines += ["", f"Grand total: {grand_total:.2f}€"]

    # --- Output ---
    report = "\n".join(lines)
    print(report)
    output_path.write_text(report + "\n", encoding="utf-8")

    csv_path = SCRIPT_DIR / "results_all.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["month", "product", "revenue"])
        writer.writerows(all_results)


if __name__ == "__main__":
    main()
