import pystray
from PIL import Image

from src import gui
from src.utils import log


def exit_by_tray_icon(icon, _):
    log.warning(f'CeleBirthday 停止运行（通过托盘图标）')
    icon.stop()
    exit(0)


tray_icon = pystray.Icon(
    'test name',
    icon=Image.open('./resources/cake_logo.ico'),
    menu=pystray.Menu(
        pystray.MenuItem('关于 CeleBirthday', gui.about_app),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('仪表盘', gui.dashboard),
        pystray.MenuItem('控制面板', gui.control_panel),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('退出程序', exit_by_tray_icon),
    )
)

log.warning(f'CeleBirthday 成功启动')
tray_icon.run()
