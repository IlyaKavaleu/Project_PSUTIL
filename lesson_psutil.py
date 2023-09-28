import os
import time

import psutil
import platform
import json
from tabulate import tabulate
from colorama import Fore, Back, Style, init

init()


def clear_screen():
    """Screen cleaning function"""
    os.system('cls' if os.name == 'nt' else 'clear')


def count_MB(count_bytes, suffix='B'):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if count_bytes < factor:
            return f"{count_bytes:.2f}{unit}{suffix}"
        count_bytes /= factor


def print_and_write_system_info(data_from_psutil):
    """Function get dict from function and get this to beautiful table like KEY-VALUE"""
    system_info = data_from_psutil

    table_data = [['Property', 'Value']]
    for prop, value in system_info.items():
        table_data.append([prop, value])
    print(Fore.YELLOW + tabulate(table_data, tablefmt='fancy_grid'))

    file = 'file_psutil.json'
    with open(file, 'a') as json_file:
        json.dump(data_from_psutil, json_file, ensure_ascii=False, indent=4)


def print_system_info():
    """Information about system"""
    uname = platform.uname()
    system_info = {
        'Title': ('=' * 40, 'System information', '=' * 40),
        'System name': uname.system,
        'Name node': uname.node,
        'Release': uname.release,
        'Version': uname.version,
        'Machine': uname.machine,
        'Processor': uname.processor,
    }
    print_and_write_system_info(system_info)


def print_cpu_info():
    """Information about processor"""
    cpufreq = psutil.cpu_freq()
    system_info = {
        'Title': ('=' * 40, 'Information about processor', '=' * 40),
        'Physical CPU': psutil.cpu_count(logical=False),
        'All CPU': psutil.cpu_count(logical=True),
        'Maximum freq': f'{cpufreq.max:.2f}MHz',
        'Minimal freq': f'{cpufreq.min:.2f} MHz',
        'Current freq': f'{cpufreq.current:.2f} MHz'
    }
    print_and_write_system_info(system_info)


def print_cpu_usage():
    """Function for displaying information about CPU load"""
    data = {}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        data[f'CPU {i}'] = percentage
    system_info = {
        'Title': ('=' * 40, 'CPU load per core', '=' * 40),
        'Total processor load': f'{psutil.cpu_percent()}%',
        'CPU': data
    }
    print_and_write_system_info(system_info)


def print_memory_info():
    """Function for displaying information about RAM"""
    svmem = psutil.virtual_memory()
    system_info = {
        'Title': ('=' * 40, 'RAM info', '=' * 40),
        'Total': count_MB(svmem.total),
        'Available': count_MB(svmem.available),
        'Used': count_MB(svmem.used),
        'Percent': f'{svmem.percent}%'
    }
    print_and_write_system_info(system_info)


def print_swap_memory():
    """Function for displaying information about swap memory"""
    swap = psutil.swap_memory()
    system_info = {
        'Title': ('=' * 40, 'Swap memory', '=' * 40),
        'Total': count_MB(swap.total),
        'Free': count_MB(swap.free),
        'Used': count_MB(swap.used),
        'Percent': swap.percent
    }
    print_and_write_system_info(system_info)


def print_disk_info():
    """Function to display disk information"""
    data = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            system_info = {
                'Title': ('=' * 40, 'Disks info', '=' * 40),
                'Disk': partition.device,
                'File system': partition.fstype,
                'Total usage': count_MB(partition_usage.total),
                'Used': count_MB(partition_usage.used),
                'Free': count_MB(partition_usage.free)
            }
        except PermissionError:
            continue
        print_and_write_system_info(system_info)


def print_network_info():
    """Function to display network information"""
    system_info = {'Title': ('=' * 40, 'Network info', '=' * 40)}
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        interface_info = {}
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                interface_info['IP'] = address.address
                interface_info['Network mask'] = address.netmask
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                interface_info['MAC-address'] = address.address
                interface_info['Network mask'] = address.netmask
                interface_info['Broadcast MAC'] = address.broadcast
        system_info[f'Interface ({interface_name})'] = interface_info

    net_io = psutil.net_io_counters()
    system_info['Total number of MB sent'] = count_MB(net_io.bytes_sent)
    system_info['Total number of GB received'] = count_MB(net_io.bytes_recv)
    print_and_write_system_info(system_info)


def main():
    """Call print_network_info() to print network information"""
    print_system_info()
    print_cpu_info()
    print_cpu_usage()
    print_memory_info()
    print_swap_memory()
    print_disk_info()
    print_network_info()


if __name__ == '__main__':
    print('='*69, 'Start system', '='*70)
    count = 0
    for x in range(10):
        time.sleep(2)
        count += 10
        print('='*69, f"Hacking system to ...{count}%", '='*70)
    time.sleep(2)
    main()
    time.sleep(2)
    print('='*69, 'Finish system', '='*70)
