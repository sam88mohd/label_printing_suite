from pathlib import Path
import pyinputplus as pyip
import csv

RESULT_DIR = Path("./results")
INPUT_DIR = Path("./input")

def read_file(filename, start_id, start_lot):
    products = {}
    start_running_number = int(start_lot[-3:])
    with open(INPUT_DIR / filename, 'r', encoding='utf-8-sig')as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.setdefault(row['FG CODE'], {})
            products[row['FG CODE']]['product_code'] = row['FG CODE']
            products[row['FG CODE']]['id'] = start_id
            products[row['FG CODE']]['lot_number'] = start_lot[:5] + \
                str(start_running_number).rjust(3, '0')
            products[row['FG CODE']]['date'] = "20261228 03/2022"
            products[row['FG CODE']]['expiry_date'] = "0013794 20220408"

            start_id += 1
            start_running_number += 1
    return products


def generate_txt_file(input, output):
    with open(RESULT_DIR / output, 'w') as f:
        max_length = 20
        for key, value in input.items():
            key = str(key)
            f.write(str(value['id']) + (" "*19) + value['lot_number'] + (" "*10) +
                    key + (" "*(max_length - len(key))) + key + (" "*((max_length - len(key)))) + value['date'] + (" "*9) +
                    value['expiry_date'] + "\n")


def main():
    filename = pyip.inputFilename("Enter input filename: ")
    start_id = pyip.inputNum(
        "Enter start_id, 7 chars long. (ex.: 1111111): ", min=7)
    start_lot = pyip.inputStr(
        "Enter start_lot (ex.: MY9IT100): ", strip=True, allowRegexes=[r'^MY[0-9A-Z]{6}'])
    output_filename = pyip.inputFilename(
        "Enter filename to be created: ")
    products = read_file(filename, start_id, start_lot)
    generate_txt_file(products, output_filename)


if __name__ == "__main__":
    main()
