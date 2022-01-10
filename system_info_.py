
from browser_history import get_history
from datetime import datetime, time
import platform , socket , re , uuid
import psutil
import getpass
import win32api
import win32file
from pprint import pprint

def get_system_info():

    dict_ = {}

    def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        try:
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
        except:pass

    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    try:
        dict_["user_name"] = getpass.getuser()
        dict_["Computer_name"] = platform.node()
        dict_["Processor_type"] = platform.processor()
        dict_["Operating_system"] = f'{platform.system()}-{platform.architecture()[0]}'
        dict_["Os_version"] = platform.release()
        dict_["ip_address"] = get_ip_address()
        dict_["mac_address"] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        svmem = psutil.virtual_memory()
        dict_["Total_Ram"] = get_size(svmem.total)
        dict_["Total_Cores"] = psutil.cpu_count()
        dict_["Boot_Time"] = str(datetime.now().strftime("%d-%m-%Y, %H:%M:%S")) 
    except:pass

    # Disk Information
    dict_disk = {}
    try:
        drive_types = {
                    win32file.DRIVE_UNKNOWN : "Unknown",
                    win32file.DRIVE_REMOVABLE : "Removable",
                    win32file.DRIVE_FIXED : "Fixed",
                    win32file.DRIVE_REMOTE : "Remote",
                    win32file.DRIVE_CDROM : "CDROM",
                    win32file.DRIVE_RAMDISK : "RAMDisk",
                    win32file.DRIVE_NO_ROOT_DIR : "The root directory does not exist."
                    }

        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        for device in drives:
            type = win32file.GetDriveType(device)
            dict_disk[device] = drive_types[type]
    except:pass

    # get all disk partitions
    partitions = psutil.disk_partitions()
    disk_lst = []
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_lst.append({"Disk_Name":partition.mountpoint,"Disk_Total_Size":get_size(partition_usage.total)})
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
    dict_['storage'] = disk_lst

    return dict_


system_information = get_system_info()

pprint(system_information)