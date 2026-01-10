import csv
import datetime
import logging
import os
import reprlib
import tomllib
import json

import dateparser
from plyer import notification


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s | %(module)s.%(funcName)s:%(lineno)d@%(threadName)s] | %(levelname)s | %(message)s',
)
log = logging.getLogger(__name__)
notify = notification.notify

with open('pyproject.toml', 'rb') as f:
    proj_info = tomllib.load(f)
VERSION = proj_info['project']['version']
VERSION_FULL = f"{proj_info['project']['name']} {proj_info['other']['version_full']}"
WEBSITE = proj_info['project']['urls']['Homepage']

DEFAULT_CONFIG_PATH = '/config/config.json'
os.makedirs(os.path.dirname(DEFAULT_CONFIG_PATH), exist_ok=True)


def _get_date_from(date_str: str) -> datetime.date | None:
    """
    从字符串中解析日期，返回 datetime.date 对象。

    Args:
        date_str (str): 日期字符串，格式为以 "YMD" 排序的任意格式日期，如 "2009/12/10"、"2012-06-20"等。

    Returns:
        datetime.date: 解析后的日期对象。
    """
    res = dateparser.parse(date_str, settings={'DATE_ORDER': 'YMD', 'STRICT_PARSING': True})
    if res is None:
        log.error(f'无法解析日期字符串 {date_str!r}，返回 None')
        return None
    return res.date()


def read_config() -> dict:
    """
    从默认配置路径读取配置文件，返回一个dict。若文件不存在，则从模板创建文件。

    Returns:
        dict: 配置文件的字典表示。
    """
    try:
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf8') as f:
            res = json.load(f)
            log.debug(f'从 {DEFAULT_CONFIG_PATH} 读取了配置 {reprlib.repr(res)}')
    except FileNotFoundError:
        log.warning(f'未找到默认配置文件 {DEFAULT_CONFIG_PATH}，从模板创建新的配置文件。')
        with open(DEFAULT_CONFIG_PATH, 'w', encoding='utf8') as f:
            json.dump({"birthday_file": ""}, f, indent=4)
        res = {"birthday_file": ""}

    return res


def read_birthdays(config: dict) -> dict[str, datetime.date | None]:
    """
    读取配置字典，返回一个dict，键为姓名，值为生日日期。

    Args:
        config (dict): 配置文件的字典表示。

    Returns:
        dict[str, datetime.date]: 键为姓名，值为生日日期的字典
    """
    try:
        with open(config["birthday_file"], 'r', encoding="utf8") as f:
            log.debug(f'读取了生日csv文件 {config["birthday_file"]}')
            reader = csv.DictReader(f)
            return {
                row['姓名']: _get_date_from(row['出生日期'])
                for row in reader
            }
    except FileNotFoundError:
        log.error(f'未找到生日csv文件 {config["birthday_file"]!r}，返回空字典。')
        return {}


def has_birthday_today(birthdays: dict[str, datetime.date | None]) -> str:
    """
    检查是否有人在今天过生日。

    Args:
        birthdays (dict[str, datetime.date | None]): 键为姓名，值为生日日期的生日列表字典。

    Returns:
        str: 如果有生日在今天，则返回当日过生日人的姓名；否则返回空字符串。
    """
    today = datetime.date.today()
    log.debug(f'从 {reprlib.repr(birthdays)} 检查是否有生日在今天 ({today!r})')
    for name, birthday in birthdays.items():
        if (today.month, today.day) == (birthday.month, birthday.day):
            log.debug(f'检测到 {name!r} 在今天（{today!r}）过生日')
            return name
    return ''
