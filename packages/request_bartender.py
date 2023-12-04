from pathlib import Path
from time import sleep
import pyinputplus as pt
import csv
import requests
import urllib3
import uuid

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
api_url = "https://pw01shs6btnap01.bdx.com/BarTender/"
result_folder = Path('./pdf')


def get_token():
    print('Getting permission from bartender...')
    auth = requests.post(url=api_url + "api/v1/Authenticate", json={
        "username": "10367319@bdx",
        "password": "kwek54321!@#$%"
    }, verify=False)

    if auth.ok:
        print("got the Token!")
        token = auth.json()['token']

    header = {
        'Authorization': 'Bearer ' + token,
    }

    return header


def get_pdf(lot, code, artwork):
    header = get_token()

    print(f"Getting code: {code} with artwork: {artwork}")
    print("Proceed to get the PDF...")

    id = uuid.uuid4().hex

    response = requests.post(url=api_url + "api/v1/print", headers=header, json={
        "libraryID": "7f4b2eb0-2b17-4b9e-bda5-ebd99f8eb02d",
        "relativePath": f"Malaysia/Strip Pack/Pouch/Variable Labels/{artwork}.btw",
        "printRequestID": id,
        "printer": "PDF",
        "startingPosition": 0,
        "copies": 0,
        "serialNumbers": 0,
        "dataEntryControls":
        {
            "ControlType": "dropdownrecordpickercontrol",
            "DataEntryControlName": "Dropdown Record Picker 1",
            "Value": "5",
        }
    }, verify=False, timeout=(100, 100))

    if response.ok:
        print("Got the PDF link")
        pdf_path = response.json()['filePath']
        pdf = requests.get(pdf_path, verify=False)

        with open(result_folder / f"{artwork}-({code}).pdf", 'wb') as file:
            file.write(pdf.content)
        print("Done saving the PDF!")
    else:
        print("Error: ", response.json())
        print("Failed to get the Print.")


def main():
    INPUT_PATH = Path("./input")
    file_path = INPUT_PATH / pt.inputFilename("Enter filename: ")
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lot = row['lot']
            code = row['code']
            artwork = row['artwork']
            get_pdf(lot, code, artwork)


if __name__ == "__main__":
    main()
