import reprlib
import datetime

import pystray
from PIL import Image

from src import gui
from src import utils


def exit_by_tray_icon(icon, _):
    utils.log.warning(f'CeleBirthday 停止运行（通过托盘图标）')
    icon.stop()
    exit(0)


tray_icon = pystray.Icon(
    'CeleBirthday',
    icon=Image.open('./resources/cake_logo.ico'),
    menu=pystray.Menu(
        pystray.MenuItem('关于 CeleBirthday', gui.about_app),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('仪表盘', lambda: gui.dashboard(config, birthdays)),
        pystray.MenuItem('控制面板', gui.control_panel),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('退出程序', exit_by_tray_icon),
    )
)
config = utils.read_config()
birthdays = utils.read_birthdays(config)
if not utils.is_valid_birthday(birthdays):
    utils.log.warning(f'从配置 {reprlib.repr(config)} 读取到的生日列表 {reprlib.repr(birthdays)} 为空')
    utils.notify(
        title='CeleBirthday 警告 - 配置文件',
        message='从生日列表文件读取到的生日列表为空或是无效记录。请前往控制面板设置一个有效的生日列表文件。',
        app_name='CeleBirthday',
        app_icon='./resources/cake_logo.ico',
    )
utils.log.debug(f'读取了配置 {reprlib.repr(config)}')
utils.log.debug(f'读取了生日列表 {reprlib.repr(birthdays)}')

if not utils.has_birthday_today(birthdays) and utils.is_valid_birthday(birthdays):
    utils.log.info(f'在今天没有任何人过生日。')
    utils.notify(
        title='CeleBirthday 状态提示',
        message=f'状态：在今天没有任何人过生日。\n下一个生日是 '
                f'{f"{nb[0]}: {nb[1].strftime('%Y-%m-%d')}" if (nb := utils.next_birthday(birthdays)) != ("", None) else "-"}。',
        app_name='CeleBirthday',
        app_icon='./resources/cake_logo.ico',
    )
else:
    today_birthday = utils.next_birthday(birthdays)
    utils.log.info(f'在今天 {today_birthday[0]} 过生日。')
    celebrate_time = datetime.time.fromisoformat(config['celebration_time'])
    gui.celebrate_today(today_birthday[0], celebrate_time)

utils.log.warning(f'CeleBirthday 成功启动')
tray_icon.run()
