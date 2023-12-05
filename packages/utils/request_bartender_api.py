from packages.utils.details import API_URL, USERNAME, PASSWORD
from halo import Halo
from spinners import Spinners
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_token():
    auth = requests.post(url=API_URL + "api/v1/Authenticate", json={
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
    response = requests.get(url=API_URL + "api/v1/printers",
                            headers=header, verify=False)

    if response.ok:
        printers = response.json()['serverPrinters']

    return printers


def get_folder_list():
    header = get_token()
    spinner = Halo(text="Getting contents list",
                   spinner=Spinners.bouncingBall.value, placement="right")
    spinner.start()
    response = requests.get(
        url=API_URL + "api/v1/libraries/7f4b2eb0-2b17-4b9e-bda5-ebd99f8eb02d", headers=header, verify=False)
    spinner.stop()

    if response.ok:
        contents = response.json()['contents']
        for content in contents:
            if 'Malaysia/Strip Pack' not in content and 'Malaysia' in content:
                print(content)
    else:
        get_folder_list()
