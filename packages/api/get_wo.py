from pathlib import Path
from time import time_ns
import pymssql
import csv


class DbCursor():
    """class for retrieve data from BarTender database and store in csv
    """

    def __init__(self, server: str, user: str, password: str):
        self.server = server
        self.user = user
        self.password = password
        self.__data = []
        self.__filtered_data = []

    @property
    def data(self):
        return self.__data

    @property
    def filtered_data(self):
        return self.__filtered_data

    def get_data(self):
        conn = pymssql.connect(self.server, self.user, self.password, "tempdb")
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            'SELECT Lot, Pcode1 FROM BDUCC_BT_NA_Datastore.dbo.MalaysiaWO')
        row = cursor.fetchone()
        while row:
            self.__data.append(row)
            row = cursor.fetchone()
        conn.close()

    def filter_data(self, product_code: str):
        assert isinstance(product_code, str), "Entered item is not string"
        for item in self.data:
            if item['Pcode1'] == product_code:
                if not any(code['Pcode1'] == product_code for code in self.__filtered_data):
                    self.__filtered_data.append(item)

    def write_to_csv(self, filtered=False):
        fieldnames = ['Lot', 'Pcode1']
        results_folder_path = Path('results')
        Path.mkdir(results_folder_path, exist_ok=True)
        filename = results_folder_path / f"WO_{str(time_ns())}.csv"
        with open(filename, 'w', encoding='UTF-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({"Lot": "LOT #", "Pcode1": "FG CODE"})
            # writer.writeheader()
            if filtered:
                writer.writerows(self.__filtered_data)
            else:
                writer.writerows(self.__data)
