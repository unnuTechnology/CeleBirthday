import functools
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

from src.utils import log


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
    panel.mainloop()


@_run_on_new_thread
def about_app():
    """显示 CeleBirthday 应用程序信息"""
    #TODO: replace with a more detailed window with buttons
    log.info(f'打开了 CeleBirthday 关于应用程序窗口')
    showinfo('关于 CeleBirthday', '在班级大屏上庆祝你同学们（当然还有你自己）的生日！')


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
    board.mainloop()
