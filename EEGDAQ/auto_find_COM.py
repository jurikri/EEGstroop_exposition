# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 14:07:40 2024

@author: PC
"""

def msmain():
    #%%
    for _ in range(2):
        try:
            import subprocess
            import pkg_resources    
            import bluetooth # https://github.com/pybluez/pybluez
            import serial
            import serial.tools.list_ports
            from pyOpenBCI import OpenBCICyton
            import time
            import threading
            import serial.tools.list_ports
            import subprocess
            import wmi
            break
            
        except:
            def install_package(package_name):
                # 패키지가 이미 설치되어 있는지 확인
                installed_packages = {pkg.key for pkg in pkg_resources.working_set}
                if package_name not in installed_packages:
                    # 패키지가 설치되어 있지 않을 경우 설치
                    subprocess.check_call(["python", "-m", "pip", "install", package_name])
                    print(f"{package_name} has been installed.")
                else:
                    # 패키지가 이미 설치되어 있음
                    print(f"{package_name} is already installed.")
            
            # 패키지 이름 설정
            package_names = ['pyOpenBCI', 'matplotlib', 'numpy', 'xmltodict', 'pyserial', 'requests', 'pandas', 'WMI']
            for package_name in package_names:
                install_package(package_name)
                
            def install_from_github(repo_url):
                """ GitHub repo에서 패키지를 설치합니다."""
                subprocess.check_call(["python", "-m", "pip", "install", "git+" + repo_url])
                print(f"Package from {repo_url} has been installed.")
                
            repo_url = "https://github.com/pybluez/pybluez.git"
            install_from_github(repo_url)
        
    def find_bluetooth_device(target_name):
        print("Searching for devices...")
        
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, \
                                                    flush_cache=True, lookup_class=False)
        
        for addr, name in nearby_devices:
            # print(f"Found {name} - {addr}")
            if name in  target_name:
                print(f"Target device '{name}' found. Address: {addr}")
                return addr
        
        print(f"Target device '{target_name}' not found.")
        return None
    
    def find_bluetooth_port(target_address):
        # WMI 초기화
        c = wmi.WMI()
        # 모든 연결된 COM 포트를 나열합니다.
        ports = serial.tools.list_ports.comports()
    
        for port in ports:
            print(port)
            try:
                # 각 포트의 PNPDeviceID를 확인합니다.
                for device in c.Win32_PnPEntity(ConfigManagerErrorCode=0):
                    if port.device in device.Name and target_address.replace(":", "") in device.PNPDeviceID:
                        return port.device
            except Exception as e:
                print(f"Error checking port {port.device}: {e}")
                continue
        return None
    
    target_name = ["BB24_140", "BB24_200"]  # 목표 블루투스 기기 이름
    target_address = find_bluetooth_device(target_name)
    port = find_bluetooth_port(target_address)
    
    if port:
        print(f"Bluetooth device {target_address} is connected on port: {port}")
    else:
        print("Could not find the Bluetooth device on any serial port.")

    return port





















