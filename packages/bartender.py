from packages.utils.details import INPUT_DIR, LOG_DIR
from packages.utils import helper, download_pdf, request_bartender_api
from datetime import datetime
import pyinputplus as pp
from packages import print_label


files = dict()

for file in INPUT_DIR.glob("*.csv"):
    files[file.name] = file.name


def main():
    date = datetime.now().strftime("%d%m%Y%M")
    counting = 0

    selection = pp.inputMenu(['Print', 'Download'], numbered=True)
    print()
    if selection == 'Print':
        server_printers = request_bartender_api.get_printer_list()
        pl = pp.inputMenu(
            choices=server_printers, prompt="Please select the printer to print:\n", numbered=True)
        print()
    lot_filename = INPUT_DIR / pp.inputMenu(
        [key for key in files], prompt="Please select the csv Filename:\n", numbered=True, blank=True)
    print()
    products = helper.get_detail_from_csv(lot_filename)

    for product in products:
        label_path, lot, fg = product
        if selection == 'Download':
            try:
                download_pdf.download_label(label_path, lot, fg)
                helper.checking_folder()
                helper.move_file(helper.get_label_name(label_path), fg)
                helper.print_done_message(
                    "Operation for label '{}' completed successfully.".format(fg))
            except Exception as err:
                counting += 1
                helper.print_error_message(
                    "Operation stop when downloading {} label.".format(fg))
                with open(LOG_DIR / "log-{}.txt".format(date), 'a') as f:
                    f.write(
                        f"{counting}) Lot: {lot}    Code: {fg}    Error: {err}\n")
        elif selection == 'Print':
            try:
                serial = pp.inputInt("Enter serial number:\n")
                print_label.print_label(
                    label_path, lot=lot, serial=serial, printer=pl, fg=fg)
                helper.print_success_message("Label successfully printed!")
            except Exception as err:
                helper.print_error_message("Error!")
            helper.wait_for_input()
            continue


if __name__ == "__main__":
    main()
