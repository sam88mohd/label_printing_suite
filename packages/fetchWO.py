from packages.api.get_wo import DbCursor
from packages.utils.details import DB_SERVER, DB_USER, DB_PASSWORD, INPUT_DIR
import csv
import pyinputplus as pp

files = dict()

for file in INPUT_DIR.glob("*.csv"):
    files[file.name] = file.name


def get_filename(file):
    return files.get(file)


def main():
    filter = pp.inputYesNo("Do you want to filter the search? (yes/no)\n")
    cursor = DbCursor(server=DB_SERVER, user=DB_USER, password=DB_PASSWORD)
    cursor.get_data()
    if filter == 'yes':
        choice = pp.inputMenu([key for key in files],
                              numbered=True, blank=True)
        filename = get_filename(choice)
        with open(INPUT_DIR / filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)
            code = list(reader)

        for item in code:
            cursor.filter_data(item[0])

        cursor.write_to_csv(filtered=True)
    else:
        cursor.write_to_csv()
    print("Done fetching result!")
