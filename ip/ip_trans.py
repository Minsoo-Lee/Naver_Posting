import requests, time, subprocess
from ui import log
from utils.decorators import sleep_after

@sleep_after()
def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        return response.text
    except Exception as e:
        return f"IP 확인 실패: {e}"

# 안드로이드 개발자 옵션 활성화 + USB 디버깅 허용 필수
def toggle_airplane_mode():
    log.append_log("비행기 모드를 활성화합니다.")
    subprocess.run(["adb", "shell", "settings", "put", "global", "airplane_mode_on", "1"])
    subprocess.run(["adb", "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE", "--ez", "state", "true"])
    time.sleep(3)
    log.append_log("비행기 모드를 비활성화합니다.")
    subprocess.run(["adb", "shell", "settings", "put", "global", "airplane_mode_on", "0"])
    subprocess.run(["adb", "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE", "--ez", "state", "false"])
    time.sleep(3)

def toggle_mobile_data():
    print("모바일 데이터를 끕니다.")
    subprocess.run(["adb", "shell", "svc", "data", "disable"])
    time.sleep(3)

    print("모바일 데이터를 켭니다.")
    subprocess.run(["adb", "shell", "svc", "data", "enable"])
    time.sleep(3)