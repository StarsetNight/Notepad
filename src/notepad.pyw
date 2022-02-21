# coding = utf-8

import os
import sys
import keyboard
import wx

AboutVersion = (
    '''
    Windows Notepad
    
    作者：Advanced_Killer（b站账号）
    ThirdBlood（GitHub账号）
    
    版本 1.03 Alpha
    更新内容：
    修复了多窗口无法正常使用的bug
    
    ThirdBlood© Studio 版权所有
    '''
)


class MainWindow(wx.Frame):
    def __init__(self, parent, id_name):
        self.file_index = 0
        self.edited_file = [None]
        wx.Frame.__init__(self, parent=None, title='Loading main program...', size=(640, 480))
        wx.Frame.SetMinSize(self, size=(320, 200))
        try:
            if sys.argv[1]:
                self.edited_file[0] = sys.argv[1]
                self.file = open(sys.argv[1], 'r', encoding='utf-8')
                self.title = 'Windows Notepad - ' + sys.argv[1]
                self.content = self.file.read()
        except IndexError:
            self.title = 'Windows Notepad - 无标题.txt'
            self.content = ''
            self.edited_file[0] = ''
        self.SetTitle(self.title)
        panel = wx.Panel(self)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        icon = wx.Icon('sources\\notepad.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.Bind(wx.EVT_CLOSE, self.warning, self)
        self.edit = wx.TextCtrl(panel, pos=(0, 0), style=wx.TE_MULTILINE)
        h_sizer.Add(self.edit, proportion=1, flag=wx.EXPAND, border=0)
        panel.SetSizer(h_sizer)
        self.edit.SetValue(self.content)

        # 设置菜单1:
        file_menu = wx.Menu()
        # wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的ID
        new = file_menu.Append(wx.ID_NEW, u"新建\tCtrl+N", u"新建一个文件")  # 添加子菜单
        new_window = file_menu.Append(wx.ID_ADD, u"新建窗口\tCtrl+Shift+N", u"新建一个窗口")
        open_option = file_menu.Append(wx.ID_OPEN, u"打开\tCtrl+O", u"打开一个文件")
        save = file_menu.Append(wx.ID_SAVE, u"保存\tCtrl+S", u"保存这个文件")
        save_as = file_menu.Append(wx.ID_SAVEAS, u"另存为\tCtrl+Shift+S", u"另存为……")
        file_menu.AppendSeparator()  # 添加分割线
        exit_app = file_menu.Append(wx.ID_EXIT, u"退出", u"终止应用程序")

        # 设置菜单2:
        edit_menu = wx.Menu()
        undo = edit_menu.Append(wx.ID_UNDO, u"撤销\tCtrl＋Z", u"撤销操作")
        redo = edit_menu.Append(wx.ID_REDO, u"重做\tCtrl＋Shift＋Z", u"重做操作")

        about_menu = wx.Menu()
        about = about_menu.Append(wx.ID_ABOUT, u"关于……", u"关于Notepad...")
        register = about_menu.Append(wx.ID_ANY, u"授权许可证", u"查看授权状态")

        # 创建菜单栏
        menu_bar = wx.MenuBar()  # 创建菜单栏
        menu_bar.Append(file_menu, u"文件")
        menu_bar.Append(edit_menu, u"编辑")
        menu_bar.Append(about_menu, u"关于")
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.OnNew, new)
        self.Bind(wx.EVT_MENU, self.OnNewWindow, new_window)
        self.Bind(wx.EVT_MENU, self.OnOpen, open_option)
        self.Bind(wx.EVT_MENU, self.OnSave, save)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, save_as)
        self.Bind(wx.EVT_MENU, self.OnExit, exit_app)
        self.Bind(wx.EVT_MENU, self.OnUndo, undo)
        self.Bind(wx.EVT_MENU, self.OnRedo, redo)
        self.Bind(wx.EVT_MENU, self.OnAbout, about)
        self.Bind(wx.EVT_MENU, self.OnLicense, register)
        self.edit.Bind(wx.EVT_TEXT, self.OnEdited)

    def OnEdited(self, event):
        if self.edit.GetValue() != self.content:
            self.SetTitle(self.title + '*')
        else:
            self.SetTitle(self.GetTitle().rstrip('*'))

    def warning(self, event):
        if self.edit.GetValue() != self.content:
            dlg = wx.MessageDialog(self, '所有未保存的改动都将被摧毁！\n确定要关闭吗？\n'
                                         '我知道这可能是习惯，但是这很危险……', '警告', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Destroy()
                del self
            dlg.Destroy()
        else:
            self.Destroy()
            del self

    def OnNew(self, event):
        if self.edit.GetValue() != self.content:
            dlg = wx.MessageDialog(self, '所有未保存的改动都将被摧毁！\n确定要继续吗？',
                                   '警告', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                title = 'Windows Notepad - 无标题.txt'
                self.SetTitle(title)
                self.edit.SetValue('')
                self.edited_file[0] = ''
            dlg.Destroy()
        else:
            title = 'Windows Notepad - 无标题.txt'
            self.SetTitle(title)
            self.edit.SetValue('')
            self.edited_file[0] = ''

    def OnNewWindow(self, event):
        self.file_index += 1
        real_name = 'main' + str(self.file_index)
        exec(real_name + ' = MainWindow(parent=None, id_name=-1)')
        exec(real_name + '.Show()')

    def OnOpen(self, event):
        dlg = wx.FileDialog(parent=None, message='选择要打开的文件',
                            defaultDir=os.getcwd(),
                            wildcard="Supported Text File *.txt|*.txt")
        if dlg.ShowModal() == wx.ID_OK:
            self.edited_file = dlg.GetPaths()
            title = 'Windows Notepad - ' + self.edited_file[0]
            self.SetTitle(title)
        else:
            return
        dlg.Destroy()
        if not os.path.exists(self.edited_file[0]):
            dlg = wx.MessageDialog(self, '创建该文件？',
                                   '找不到文件', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_NO:
                return
            dlg.Destroy()
        try:
            with open(self.edited_file[0], 'r', encoding='utf-8') as opened_file:
                self.content = opened_file.read()
                self.edit.SetValue(self.content)
        except PermissionError:
            wx.MessageBox('权限不足，请查看是否有相应目录的权限')

    def OnSave(self, event):
        try:
            if self.edited_file[0]:
                self.file = open(self.edited_file[0], 'w+', encoding='utf-8')
                self.file.write(self.edit.GetValue())
                self.file.close()
                self.content = self.edit.GetValue()
            else:
                dlg = wx.FileDialog(parent=None, message='选择要保存文件的目录',
                                    defaultDir=os.getcwd(),
                                    wildcard="文本文件 *.txt|*.txt")
                if dlg.ShowModal() == wx.ID_OK:
                    resource = dlg.GetPaths()
                else:
                    return
                dlg.Destroy()
                if not os.path.exists(resource[0]):
                    dlg = wx.MessageDialog(self, '创建该文件？',
                                           '找不到文件', wx.YES_NO | wx.ICON_QUESTION)
                    if dlg.ShowModal() == wx.ID_NO:
                        return
                    dlg.Destroy()
                self.file = open(resource[0], 'w+', encoding='utf-8')
                self.file.write(self.edit.GetValue())
                self.file.close()
                self.edited_file[0] = resource[0]
                title = 'Windows Notepad - ' + self.edited_file[0]
                self.SetTitle(title)
                self.content = self.edit.GetValue()
                self.edited_file[0] = resource[0]
            self.SetTitle(self.GetTitle().rstrip('*'))
        except PermissionError:
            wx.MessageBox('权限不足，请查看是否有相应目录的权限')
            self.file.close()

    def OnSaveAs(self, event):
        dlg = wx.FileDialog(parent=None, message='将文件另存为……',
                            defaultDir=os.getcwd(),
                            wildcard="文本文件 *.txt|*.txt")
        if dlg.ShowModal() == wx.ID_OK:
            resource = dlg.GetPaths()
        else:
            return
        dlg.Destroy()
        if not os.path.exists(resource[0]):
            dlg = wx.MessageDialog(self, '创建该文件？',
                                   '找不到文件', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_NO:
                return
            dlg.Destroy()
        written_file = open(resource[0], 'w+', encoding='utf-8')
        written_file.write(self.edit.GetValue())
        written_file.close()
        self.edited_file[0] = resource[0]
        title = 'Windows Notepad - ' + self.edited_file[0]
        self.SetTitle(title)
        self.content = self.edit.GetValue()
        self.SetTitle(self.GetTitle().rstrip('*'))

    def OnExit(self, event):
        if self.edit.GetValue() != self.content:
            dlg = wx.MessageDialog(self, '所有未保存的改动都将被摧毁！\n你还要继续吗？'
                                         '\n为了安全，请在退出前保存你的文件', '警告',
                                   wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Destroy()
                del self
            dlg.Destroy()
        else:
            self.Destroy()
            del self

    @staticmethod
    def OnLicense(event):
        wx.MessageBox('哈哈，你被骗啦，根本没有授权许可证……\n'
                      '好消息是，这个软件不收费（本来就不应该收费……）')

    @staticmethod
    def OnUndo(event):
        keyboard.send('Ctrl+Z')

    @staticmethod
    def OnRedo(event):
        keyboard.send('Ctrl+Shift+Z')

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, AboutVersion,
                               '关于Notepad', wx.YES_DEFAULT | wx.ICON_QUESTION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    main = MainWindow(parent=None, id_name=-1)
    main.Show()
    app.MainLoop()
