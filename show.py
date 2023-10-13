from tabulate import tabulate
from colorama import Fore, Back, Style, init


def show(dates):
    """Print all information to the console"""
    table_data = [['Property', 'Value']]
    for category, func in dates.items():
        data = func()
        table_data.append(['', ''])
        for prop, value in data.items():
            table_data.append([prop, value])
    print(Fore.YELLOW + tabulate(table_data, tablefmt='fancy_grid'))