import psutil
from func_converter import count_MB
from decorator import to_json
import platform


@to_json('get_system_info.json')
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


@to_json('get_cpu_info.json')
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


@to_json('get_cpu_usage.json')
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


@to_json('get_memory_info.json')
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


@to_json('get_swap_memory.json')
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


@to_json('get_disk_info.json')
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


@to_json('get_network_info.json')
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
        'system_info': get_system_info,
        'cpu_info': get_cpu_info,
        'cpu_usage': get_cpu_usage,
        'memory_info': get_memory_info,
        'swap_memory': get_swap_memory,
        'disk_info': get_disk_info,
        'network_info': get_network_info,
    }
    return functions