from dataclasses import dataclass
import wx

@dataclass
class AccountWebSection:
    parent_panel: wx.Panel
    child_panel: wx.Panel
    parent_sizer: wx.Sizer
    account_button: wx.Button
    account_list: wx.ListCtrl
    web_button: wx.Button
    web_list: wx.ListCtrl