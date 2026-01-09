from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import logging

import pystray
from PIL import Image

import gui


def exit_by_tray_icon(icon, _):
    log.warning(f'CeleBirthday 停止运行（通过托盘图标）')
    icon.stop()
    exit(0)


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s | %(module)s.%(funcName)s:%(lineno)d] %(levelname)s | %(message)s',
)
log = logging.getLogger(__name__)

tray_icon = pystray.Icon(
    'test name',
    icon=Image.open('./resources/cake_logo.ico'),
    menu=pystray.Menu(
        pystray.MenuItem('控制面板', control_panel),
        pystray.MenuItem('退出', exit_by_tray_icon),
    )
)

log.warning(f'CeleBirthday 成功启动')
tray_icon.run_detached()
