import socket
from multiprocessing.connection import Client

import requests
import re
from ppadb.
import time
import os

def trans_ip():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    device = devices[0]

    print(f"Serial Number = {device.serial}")

    ip = requests.get("https://api.ipify.org", timeout=5).text
    print(f"외부 IP = {ip}")

    # usb 테더링 제어
    os.system("svc data disable")
    time.sleep(5)
    os.system("svc data enable")
    time.sleep(5)

    # 에어플레인 모드 ON
    device.shell("svc data disable")
    device.shell("adb shell settings put global airplane_mode_on 1")
    device.shell("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true")
    device.shell("adb shell cmd connectivity airplane-mode enable")

    time.sleep(5)

    # 에어플레인 모드 OFF
    device.shell("svc data enable")
    device.shell("adb shell settings put global airplane_mode_on 0")
    device.shell("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false")
    device.shell("adb shell cmd connectivity airplane-mode disable")

    time.sleep(5)

    ip = requests.get("https://api.ipify.org", timeout=5).text
    print(f"외부 IP = {ip}")
