import multiprocessing
import sys
import platform,socket,re,uuid,json,psutil
from dotenv import load_dotenv
from fastapi import APIRouter
import subprocess
import requests

load_dotenv()
systemrouter = APIRouter(prefix="/system", tags=["System"])


@systemrouter.get("/info")
async def get_platform():
    return json.loads(getSystemInfo())


def getSystemInfo():
    info={}
    info['platform']=platform.system()
    if platform.system() == 'Darwin':
        info['os'] = get_mac_info()
    elif platform.system() == 'Windows':
        info['os'] = get_windows_info()
    elif platform.system() == 'Linux':
        info['os'] = get_linux_info()
    info['platform-release']=platform.release()
    info['hostname']=socket.gethostname()
    info['public-ip-address']=get_public_ip()
    info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
    info['processor']=get_processor_details()
    info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    return json.dumps(info)

def get_mac_info():
    productVersion = subprocess.run(['sw_vers', '-productVersion'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    buildVersion = subprocess.run(['sw_vers', '-buildVersion'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    productName = subprocess.run(['sw_vers', '-productName'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    mac_info={'productVersion':productVersion,'buildVersion':buildVersion,'productName':productName}
    return mac_info

def get_windows_info():
    # Get product version
    product_version ="unnown" #subprocess.run(['powershell', '-Command', 'Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion" | Select-Object ProductName, DisplayVersion'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    
    # Get build version (same as product version in this context)
    build_version = "unknown" #subprocess.run(['powershell', '-Command', 'Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion" | Select-Object ProductName, DisplayVersion'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    
    # Get product name
    product_name = "unknown" #subprocess.run(['powershell', '-Command', 'Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion" | Select-Object ProductName'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    
    windows_info = {
        'productVersion': product_version,
        'buildVersion': build_version,
        'productName': product_name
    }
    return windows_info

def get_linux_info():
    # # Get product version (kernel version)
    # kernel_version = subprocess.run(['uname', '-r'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    
    # # Read /etc/os-release for more detailed information
    # os_info = subprocess.run(['cat', '/etc/os-release'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()
    
    # # Parse the output of /etc/os-release to extract product name and version
    parsed_info = {}
    # for line in os_info.split('\n'):
    #     if '=' in line:
    #         key, value = line.split('=', 1)
    #         parsed_info[key] = value.strip('"')
    
    linux_info = {
        'productVersion': parsed_info.get('PRODUCT', 'unknown'),
        'buildVersion': parsed_info.get('VERSION', 'unknown'),
        'productName': parsed_info.get('NAME', 'unknown')
    }
    return linux_info

def get_processor_details():
  """Returns a dictionary containing the processor details of the system"""
  processor = {}
  processor['name'] = platform.processor()
  processor['architecture'] = platform.machine()
  processor['cores'] = multiprocessing.cpu_count()
  processor['threads'] = psutil.cpu_count(logical=True)
  return processor

def get_public_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]