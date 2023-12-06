from packages.utils.details import BASE_URL, USERNAME, PASSWORD
from packages.utils.helper import write_to_csv
from halo import Halo
from spinners import Spinners
import pyinputplus as pp
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_token():
    auth = requests.post(url=BASE_URL + "api/v1/Authenticate", json={
        "username": "{}@bdx".format(USERNAME),
        "password": PASSWORD
    }, verify=False)

    if auth.ok:
        token = auth.json()['token']

    header = {
        'Authorization': 'Bearer ' + token,
    }

    return header


def get_printer_list():
    header = get_token()
    response = requests.get(url=BASE_URL + "api/v1/printers",
                            headers=header, verify=False)

    if response.ok:
        printers = response.json()['serverPrinters']

    return printers


def get_folder_list():
    header = get_token()
    spinner = Halo(text="Getting Print Portal folder list ",
                   spinner=Spinners.bouncingBar.value, placement="right")
    spinner.start()
    response = requests.get(
        url=BASE_URL + "api/v1/libraries/7f4b2eb0-2b17-4b9e-bda5-ebd99f8eb02d", headers=header, verify=False)
    spinner.stop()

    if response.ok:
        contents = response.json()['contents']
        malaysia_file = [
            content for content in contents if 'Malaysia' in content]
        for file in malaysia_file:
            print(file)
        save = pp.inputYesNo(
            prompt="Want to save the list?\n")
        if save == 'yes':
            write_to_csv('path', data=malaysia_file)
    else:
        get_folder_list()
