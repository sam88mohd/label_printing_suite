from pathlib import Path
from libs.browser import Browser
import csv


class FileReader:
    __items = []

    def __init__(self, path):
        self.path = Path(path)
        with open(self.path, 'r', encoding="utf-8-sig", newline='') as f:
            data = csv.DictReader(f)
            for row in data:
                browser = Browser(row['FG CODE'])
                self.__items.append(browser)

    @property
    def items(self):
        return self.__items
