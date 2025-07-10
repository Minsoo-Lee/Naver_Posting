import socket
import requests
import re
from ppadb.client import Client as AdbClient
import time
import os

def trans_ip():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    device = devices[0]

    print(f"Serial Number = {device.serial}")

    req = requests.get("http://ipconfig.kr")
    print("외부 IP = ", re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])

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

    req = requests.get("http://ipconfig.kr")
    print("외부 IP = ", re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])
