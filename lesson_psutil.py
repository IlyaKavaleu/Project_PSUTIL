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


def get_system_info():
    """Information about system"""
    uname = platform.uname()
    system_info = {
        'system_name': uname.system,
        'name_node': uname.node,
        'release': uname.release,
        'version': uname.version,
        'machine': uname.machine,
        'processor': uname.processor,
    }
    return system_info


def get_cpu_info():
    """Information about processor"""
    cpufreq = psutil.cpu_freq()
    system_info = {
        'physical_CPU': psutil.cpu_count(logical=False),
        'all_CPU': psutil.cpu_count(logical=True),
        'maximum_freq': f'{cpufreq.max:.2f}MHz',
        'minimal_freq': f'{cpufreq.min:.2f} MHz',
        'current_freq': f'{cpufreq.current:.2f} MHz'
    }
    return system_info


def get_cpu_usage():
    """Function for displaying information about CPU load"""
    data = {}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        data[f'cpu {i}'] = percentage
    system_info = {
        'total_processor_load': f'{psutil.cpu_percent()}%',
        'data_CPU': data
    }
    return system_info


def get_memory_info():
    """Function for displaying information about RAM"""
    svmem = psutil.virtual_memory()
    system_info = {
        'total': count_MB(svmem.total),
        'available': count_MB(svmem.available),
        'used': count_MB(svmem.used),
        'percent': f'{svmem.percent}%'
    }
    return system_info


def get_swap_memory():
    """Function for displaying information about swap memory"""
    swap = psutil.swap_memory()
    system_info = {
        'total': count_MB(swap.total),
        'free': count_MB(swap.free),
        'used': count_MB(swap.used),
        'percent': swap.percent
    }
    return system_info


def get_disk_info():
    """Function to display disk information"""
    system_info = {}
    partitions = psutil.disk_partitions()
    for index, partition in enumerate(partitions):
        partition_usage = psutil.disk_usage(partition.mountpoint)
        data_disks = {
            'disk': partition.device,
            'file_system': partition.fstype,
            'total_usage': count_MB(partition_usage.total),
            'used': count_MB(partition_usage.used),
            'free': count_MB(partition_usage.free)
        }
        system_info[f"disk_{index + 1}"] = data_disks
    return system_info


def get_network_info():
    """Function to display network information"""
    system_info = {}
    addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in addrs.items():
        interface_info = {}
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                interface_info['ip'] = address.address
                interface_info['network_mask'] = address.netmask
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                interface_info['mac_address'] = address.address
                interface_info['network_mask'] = address.netmask
                interface_info['broadcast_MAC'] = address.broadcast
        system_info[f'interface ({interface_name})'] = interface_info

    net_io = psutil.net_io_counters()
    system_info['total_number_of_MB_sent'] = count_MB(net_io.bytes_sent)
    system_info['total_number_of_GB_received'] = count_MB(net_io.bytes_recv)
    return system_info


def all_func():
    """Collect all functions into one dict"""
    functions = {
        'system_info': (get_system_info, 'get_system_info.json'),
        'cpu_info': (get_cpu_info, 'get_cpu_info.json'),
        'cpu_usage': (get_cpu_usage, 'get_cpu_usage.json'),
        'memory_info': (get_memory_info, 'get_memory_info.json'),
        'swap_memory': (get_swap_memory, 'get_swap_memory.json'),
        'disk_info': (get_disk_info, 'get_disk_info.json'),
        'network_info': (get_network_info, 'get_network_info.json'),
    }
    return functions


def to_json(dates):
    """Write all to another JSON files"""
    for category, (func, filename) in dates.items():
        data = func()
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)


def show(dates):
    """Print all information to the console"""
    table_data = [['Property', 'Value']]
    for category, (func, _) in dates.items():
        category_data = func()
        table_data.append(['', ''])
        for prop, value in category_data.items():
            table_data.append([prop, value])
    print(Fore.YELLOW + tabulate(table_data, tablefmt='fancy_grid'))


def main():
    show(all_func())
    to_json(all_func())


if __name__ == '__main__':
    print('=' * 69, 'Start system', '=' * 70)
    # count = 0
    # for x in range(10):
    #     time.sleep(2)
    #     count += 10
    #     print('=' * 69, f"Hacking system to ...{count}%", '=' * 70)
    time.sleep(2)
    main()
    time.sleep(2)
    print('=' * 69, 'Finish system', '=' * 70)
