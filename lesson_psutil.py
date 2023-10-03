import os
import time
import psutil
import platform
import json
from tabulate import tabulate
from colorama import Fore, Back, Style, init

init()


def count_MB(count_bytes, suffix='B'):
    """A counting function that converts bytes into GB, if necessary"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if count_bytes < factor:
            return f"{count_bytes:.2f}{unit}{suffix}"
        count_bytes /= factor


def system_info():
    """Information about system"""
    uname = platform.uname()
    get_system_info = {
        'system_name': uname.system,
        'name_node': uname.node,
        'release': uname.release,
        'version': uname.version,
        'machine': uname.machine,
        'processor': uname.processor,
    }
    return get_system_info


def cpu_info():
    """Information about processor"""
    cpufreq = psutil.cpu_freq()
    get_system_info = {
        'physical_CPU': psutil.cpu_count(logical=False),
        'all_CPU': psutil.cpu_count(logical=True),
        'maximum_freq': f'{cpufreq.max:.2f}MHz',
        'minimal_freq': f'{cpufreq.min:.2f} MHz',
        'current_freq': f'{cpufreq.current:.2f} MHz'
    }
    return get_system_info


def cpu_usage():
    """Function for displaying information about CPU load"""
    data = {}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        data[f'CPU {i}'] = percentage
    get_system_info = {
        'total_processor_load': f'{psutil.cpu_percent()}%',
        'data_CPU': data
    }
    return get_system_info


def memory_info():
    """Function for displaying information about RAM"""
    svmem = psutil.virtual_memory()
    get_system_info = {
        'total': count_MB(svmem.total),
        'available': count_MB(svmem.available),
        'used': count_MB(svmem.used),
        'percent': f'{svmem.percent}%'
    }
    return get_system_info


def swap_memory():
    """Function for displaying information about swap memory"""
    swap = psutil.swap_memory()
    get_system_info = {
        'total': count_MB(swap.total),
        'free': count_MB(swap.free),
        'used': count_MB(swap.used),
        'percent': swap.percent
    }
    return get_system_info


def disk_info():
    """Function to display disk information"""
    data = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            get_system_info = {
                'disk': partition.device,
                'file_system': partition.fstype,
                'total_usage': count_MB(partition_usage.total),
                'used': count_MB(partition_usage.used),
                'free': count_MB(partition_usage.free)
            }
        except PermissionError:
            continue
        return get_system_info


def network_info():
    """Function to display network information"""
    get_system_info = {}
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        interface_info = {}
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                interface_info['ip'] = address.address
                interface_info['network_mask'] = address.netmask
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                interface_info['mac_address'] = address.address
                interface_info['network_mask'] = address.netmask
                interface_info['broadcast_MAC'] = address.broadcast
        get_system_info[f'interface ({interface_name})'] = interface_info

    net_io = psutil.net_io_counters()
    get_system_info['total_number_of_MB_sent'] = count_MB(net_io.bytes_sent)
    get_system_info['total_number_of_GB_received'] = count_MB(net_io.bytes_recv)
    return get_system_info


def all_func():
    """We collect all functions into one dict"""
    functions = {
        'System Info': (system_info, 'system_info.json'),
        'CPU Info': (cpu_info, 'cpu_info.json'),
        'CPU Usage': (cpu_usage, 'cpu_usage.json'),
        'Memory Info': (memory_info, 'memory_info.json'),
        'Swap Memory': (swap_memory, 'swap_memory.json'),
        'Disk Info': (disk_info, 'disk_info.json'),
        'Network Info': (network_info, 'network_info.json'),
    }
    return functions


def write_to_json(dates=None):
    """Function get data and write all to another JSON files"""
    if dates is None:
        dates = dates
    for category, (func, filename) in dates.items():
        data = func()
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)


def func_print_to_console(dates=None):
    """Print all information to the console"""
    if dates is None:
        dates = dates
    table_data = [['Property', 'Value']]
    for category, (func, _) in dates.items():
        category_data = func()
        table_data.append(['', ''])
        for prop, value in category_data.items():
            table_data.append([prop, value])
    print(Fore.YELLOW + tabulate(table_data, tablefmt='fancy_grid'))


def main():
    func_print_to_console(all_func())
    write_to_json(all_func())


if __name__ == '__main__':
    print('=' * 69, 'Start system', '=' * 70)
    count = 0
    for x in range(10):
        time.sleep(2)
        count += 10
        print('=' * 69, f"Hacking system to ...{count}%", '=' * 70)
    time.sleep(2)
    main()
    time.sleep(2)
    print('=' * 69, 'Finish system', '=' * 70)
