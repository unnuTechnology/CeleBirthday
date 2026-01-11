import datetime
import functools
import threading
import traceback
import webbrowser
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import sv_ttk
import darkdetect as dd

from src import utils


def _run_on_new_thread(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


def _err_reported(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            utils.log.critical(f'发生不可恢复的异常：{e.__class__.__qualname__}: {e}')
            utils.log.debug(traceback.format_exc())
            messagebox.showerror('CeleBirthday 发生错误',
                                 f'CeleBirthday 发生不可恢复的异常：{e.__class__.__qualname__}: {e}\n'
                                 f'点击 OK 来结束程序。以下是栈错误信息。',
                                 detail=traceback.format_exc(),
                                 icon='error')
            raise
    return wrapper


@_run_on_new_thread
@_err_reported
def control_panel():
    panel = Tk()
    panel.title('CeleBirthday 控制面板')
    panel.geometry('600x500')
    panel.resizable(False, False)
    panel.iconbitmap('./resources/cake_logo.ico')

    def on_closing():
        utils.log.info(f'关闭了 CeleBirthday 控制面板')
        panel.destroy()

    panel.protocol('WM_DELETE_WINDOW', on_closing)

    utils.log.info(f'打开了 CeleBirthday 控制面板')
    sv_ttk.set_theme(dd.theme())
    panel.mainloop()


@_run_on_new_thread
@_err_reported
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
    Label(about, text=utils.VERSION_FULL, font=('Bahnschrift Light', 16, 'normal')).pack(pady=2)
    Separator(about, orient='horizontal').pack(fill=X, padx=20, pady=5)
    Label(about, text='©2026 unnuTechnology | MIT License', font=('Bahnschrift Light', 16, 'normal')).pack(pady=2)
    Label(about, text='在班级大屏上庆祝你同学们（当然还有你自己）的生日！', font=('Bahnschrift Light', 16, 'normal')).pack(
        pady=2)
    Button(about, text='项目仓库主页', command=lambda: webbrowser.open(utils.WEBSITE)).pack(
        padx=(20, 10), pady=(300, 20), expand=True, anchor=S, fill=BOTH, side=LEFT)
    Button(about, text='报告问题', command=lambda: webbrowser.open(utils.WEBSITE + '/issues')).pack(
        padx=(10, 20), pady=(300, 20), expand=True, anchor=S, fill=BOTH, side=RIGHT)

    def on_closing():
        utils.log.info(f'关闭了 CeleBirthday 关于应用程序窗口')
        about.destroy()

    about.protocol('WM_DELETE_WINDOW', on_closing)

    utils.log.info(f'打开了 CeleBirthday 关于应用程序窗口')
    sv_ttk.set_theme(dd.theme())
    about.mainloop()


@_run_on_new_thread
@_err_reported
def dashboard(config, birthdays):
    """显示 CeleBirthday 仪表盘"""
    board = Tk()
    board.title('CeleBirthday 仪表盘')
    board.geometry('700x500')
    board.resizable(False, False)
    board.iconbitmap('./resources/cake_logo.ico')

    ok_img = PhotoImage(file='./resources/ok.png')
    ok_label = Label(board, image=ok_img)
    ok_label.pack(padx=20, side=LEFT, anchor=W)

    Label(board, text='CeleBirthday 正在运行', font=('Bahnschrift', 28, 'bold')).pack(padx=10, pady=(20, 5))
    Separator(board, orient='horizontal').pack(fill=X, padx=(0, 20), pady=5)
    Label(board, text=f'今日过生日人：{utils.has_birthday_today(birthdays) if utils.has_birthday_today(birthdays) else "-"}',
          font=('Bahnschrift', 12, 'normal')).pack(padx=20, pady=5)
    Label(board, text=f'下一个生日：{f"{nb[0]}: {nb[1].strftime('%Y-%m-%d')}" if (nb := utils.next_birthday(birthdays)) != ("", None) else "-"}',
          font=('Bahnschrift', 12, 'normal')).pack(padx=20, pady=5)
    Label(board, text=f'系统时间：{datetime.date.today().strftime("%Y-%m-%d")}',
          font=('Bahnschrift', 12, 'normal')).pack(padx=20, pady=(20, 5))

    def on_closing():
        utils.log.info(f'关闭了 CeleBirthday 仪表盘')
        board.destroy()

    board.protocol('WM_DELETE_WINDOW', on_closing)

    utils.log.info(f'打开了 CeleBirthday 仪表盘')
    sv_ttk.set_theme(dd.theme())
    board.mainloop()


@_run_on_new_thread
@_err_reported
def celebrate_today(people: str, celebrate_time: datetime.time):
    """在指定时间庆祝今天过生日的人"""
    now = datetime.datetime.now().time()

    if now >= celebrate_time:
        utils.log.warning(f'当前时间 {now} 晚于指定时间 {celebrate_time}，无法庆祝 {people} 过生日。')
        utils.notify(
            title='CeleBirthday 警告',
            message=f'当前时间 {now} 晚于指定时间 {celebrate_time}，无法庆祝 {people} 过生日。',
            app_name='CeleBirthday',
            app_icon='./resources/cake_logo.ico'
        )
        return
    else:
        now = datetime.datetime.now().time()
        rest_time = (utils.total_s(celebrate_time) - utils.total_s(now))
        utils.log.info(f'将在 {celebrate_time} ({rest_time:.2f}s 后) 庆祝 {people} 过生日')
        utils.notify(
            title='CeleBirthday 通知',
            message=f'今日将在 {celebrate_time} ({rest_time:.2f}s 后) 庆祝 {people} 的生日！',
            app_name='CeleBirthday',
            app_icon='./resources/cake_logo.ico'
        )

    now = datetime.datetime.now().time()  # 重新计算避免延迟
    rest_time = (utils.total_s(celebrate_time) - utils.total_s(now))
    threading.Timer(rest_time, celebrate, args=(people, )).start()


@_run_on_new_thread
@_err_reported
def celebrate(people: str):
    """在指定时间庆祝今天过生日的人"""
    cele = Tk()

    cele.title('CeleBirthday 庆祝')
    cele.geometry('400x200')
    cele.resizable(False, False)
    cele.iconbitmap('./resources/cake_logo.ico')

    cele.mainloop()
