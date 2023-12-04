from packages import get_product_links, open_link, generate_wo, search_family, bartender, fetchWO
import pyinputplus as pp


def prompt_quit():
    print("Do you want to quit? (Y/N)")
    res = pp.inputYesNo()
    if res == 'yes':
        quit()
    else:
        return res


def switch(choice):
    return menu.get(choice)()


menu = {
    "Get product link in Master Control": get_product_links.main,
    "Open links": open_link.main,
    "Generate Work order": generate_wo.main,
    "Search by Family": search_family.main,
    "get pdf from BarTender": bartender.main,
    "Get WO from BarTender DB": fetchWO.main,
    "Quit": quit
}


def print_message():
    exit = "no"
    message = "Label Printing Suites".center(100, '*')
    print(message, end='\n\n')
    while (exit != "yes"):
        choice = pp.inputMenu([key for key in menu], numbered=True)
        switch(choice)
        exit = prompt_quit()


print_message()
