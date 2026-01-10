import functools
import threading
import webbrowser
from tkinter import *
from tkinter.ttk import *

import sv_ttk
import darkdetect as dd

from src.utils import *


def _run_on_new_thread(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


@_run_on_new_thread
def control_panel():
    panel = Tk()
    panel.title('CeleBirthday 控制面板')
    panel.geometry('600x500')
    panel.resizable(False, False)
    panel.iconbitmap('./resources/cake_logo.ico')

    def on_closing():
        log.info(f'关闭了 CeleBirthday 控制面板')
        panel.destroy()

    panel.protocol('WM_DELETE_WINDOW', on_closing)

    log.info(f'打开了 CeleBirthday 控制面板')
    sv_ttk.set_theme(dd.theme())
    panel.mainloop()


@_run_on_new_thread
def about_app():
    """显示 CeleBirthday 应用程序信息"""
    about = Tk()
    about.title('关于 CeleBirthday')
    about.geometry('800x600')
    about.resizable(False, False)
    about.iconbitmap('./resources/cake_logo.ico')

    logo = PhotoImage(file='./resources/about_poster.png')
    logo_label = Label(about, image=logo)
    logo_label.pack(padx=(0, 10), side=LEFT, anchor=W)

    Label(about, text='CeleBirthday', font=('Bahnschrift', 48, 'bold')).pack(pady=10)
    Label(about, text=VERSION_FULL, font=('Bahnschrift Light', 16, 'normal')).pack(pady=2)
    Separator(about, orient='horizontal').pack(fill=X, padx=20, pady=5)
    Label(about, text='©2026 unnuTechnology | MIT License', font=('Bahnschrift Light', 16, 'normal')).pack(pady=2)
    Label(about, text='在班级大屏上庆祝你同学们（当然还有你自己）的生日！', font=('Bahnschrift Light', 16, 'normal')).pack(pady=2)
    Button(about, text='项目仓库主页', command=lambda: webbrowser.open(WEBSITE)).pack(
        padx=(20, 10), pady=(300, 20), expand=True, anchor=S, fill=BOTH, side=LEFT)
    Button(about, text='报告问题', command=lambda: webbrowser.open(WEBSITE+'/issues')).pack(
        padx=(10, 20), pady=(300, 20), expand=True, anchor=S, fill=BOTH, side=RIGHT)

    def on_closing():
        log.info(f'关闭了 CeleBirthday 关于应用程序窗口')
        about.destroy()

    about.protocol('WM_DELETE_WINDOW', on_closing)

    log.info(f'打开了 CeleBirthday 关于应用程序窗口')
    sv_ttk.set_theme(dd.theme())
    about.mainloop()


@_run_on_new_thread
def dashboard():
    """显示 CeleBirthday 仪表盘"""
    board = Tk()
    board.title('CeleBirthday 仪表盘')
    board.geometry('500x300')
    board.resizable(False, False)
    board.iconbitmap('./resources/cake_logo.ico')

    def on_closing():
        log.info(f'关闭了 CeleBirthday 仪表盘')
        board.destroy()

    board.protocol('WM_DELETE_WINDOW', on_closing)

    log.info(f'打开了 CeleBirthday 仪表盘')
    sv_ttk.set_theme(dd.theme())
    board.mainloop()
