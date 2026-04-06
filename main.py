import ui.window as window
import wx
from auth.auth_window import AuthDialog

def open_auth_dialog():
    auth_dialog = AuthDialog()
    auth_dialog.ShowModal()
    result = auth_dialog.auth_success
    auth_dialog.Destroy()
    return result


if __name__ == "__main__":
    app = wx.App(False)
    # 내 환경에서 테스트 할 땐 주석처리
    frame = window.MainFrame()
    frame.Show()
    app.MainLoop()

    # 배포 시 주석처리 해제
    # if open_auth_dialog():
    #     print("인증 성공. 메인 실행")
    #     frame = window.MainFrame()
    #     frame.Show()
    #     app.MainLoop()
    # else:
    #     print("인증 실패. 종료합니다.")
