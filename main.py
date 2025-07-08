import ui.window as window
import wx

if __name__ == "__main__":
    app = wx.App(False)
    frame = window.MainFrame()
    app.MainLoop()
    # import google.generativeai as genai
    # import os
    #
    # genai.configure(api_key=os.environ.get("API_KEY"))
    #
    # print("generateContent를 지원하는 모델 목록:")
    # for m in genai.list_models():
    #     if "generateContent" in m.supported_generation_methods:
    #         print(f"모델 이름: {m.name}")


