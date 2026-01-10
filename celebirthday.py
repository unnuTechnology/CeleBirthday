import pystray
from PIL import Image

from src import gui
from src.utils import *


def exit_by_tray_icon(icon, _):
    log.warning(f'CeleBirthday 停止运行（通过托盘图标）')
    icon.stop()
    exit(0)


tray_icon = pystray.Icon(
    'CeleBirthday',
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
config = read_config()
birthdays = read_birthdays(config)
if not birthdays:
    log.warning(f'从配置 {reprlib.repr(config)} 读取到的生日列表 {reprlib.repr(birthdays)} 为空')
    #TODO: ⬇️does not run as intended
    tray_icon.notify('从生日列表文件读取到的生日列表为空。请前往控制面板设置一个有效的生日列表文件。', 'CeleBirthday')

log.warning(f'CeleBirthday 成功启动')
tray_icon.run()
