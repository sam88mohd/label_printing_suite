from packages.utils.details import INPUT_DIR, SEVEN_URL_PATH, TEN_URL_PATH, P7215_PHASE1_URL_PATH, P7215_PHASE2_URL_PATH, P7128_URL_PATH, LOG_DIR
from packages.utils import helper, download_pdf, request_bartender_api
from datetime import datetime
import pyinputplus as pp
from packages import prints

choices = {
    'Bell-Mark PDF 7 lane':  SEVEN_URL_PATH,
    'Bell-Mark PDF 10 lane': TEN_URL_PATH,
    'Bell-Mark PDF Project 7215 - Phase 1': P7215_PHASE1_URL_PATH,
    'Bell-Mark PDF Project 7215 - Phase 2': P7215_PHASE2_URL_PATH,
    'Bell-Mark PDF Project 7182': P7128_URL_PATH
}


def selected_path(path):
    return choices.get(path)


files = dict()

for file in INPUT_DIR.glob("*.csv"):
    files[file.name] = file.name


def main():
    date = datetime.now().strftime("%d%m%Y%M")

    selection = pp.inputMenu(['Print', 'Download'], numbered=True)

    if selection == 'Download':
        path = pp.inputMenu([key for key in choices],
                            prompt="Please select one Category of the following:\n", numbered=True)

    server_printers = request_bartender_api.get_printer_list()
    pl = pp.inputMenu(
        choices=server_printers, prompt="Please select the printer to print:\n", numbered=True)

    lot_filename = INPUT_DIR / pp.inputMenu(
        [key for key in files], prompt="Please select the csv Filename:\n", numbered=True, blank=True)

    products = helper.get_detail_from_csv(lot_filename)

    counting = 0
    for product in products:
        label, lot, fg = product
        if selection == 'Download':
            url = selected_path(path)
            try:
                download_pdf.download_label(url, label, lot, fg)
                helper.checking_folder()
                helper.move_file(label, fg)
                helper.print_done_message(
                    "Operation for label '{}-{}' completed successfully.".format(label, fg))
            except Exception as err:
                counting += 1
                helper.print_error_message(
                    "Operation stop when downloading {}-{} label.".format(label, fg))
                with open(LOG_DIR / "log-{}.txt".format(date), 'a') as f:
                    f.write(
                        f"{counting}) Label: {label}    Lot: {lot}    Code: {fg}    Error: {err.args}\n")
        elif selection == 'Print':
            while cont:
                try:
                    serial = pp.inputInt("Enter serial number:\n")
                    prints.print_label(label_type=label,
                                       lot=lot, serial=serial, printer=pl)
                    helper.wait_for_loading()
                    helper.print_success_message("Label successfully printed!")
                except Exception as err:
                    helper.print_error_message("Error!")
                cont = pp.inputBool(
                    prompt="Continue next print?\n", trueVal='yes', falseVal='no')


if __name__ == "__main__":
    main()
