import logging
import tomllib


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s | %(module)s.%(funcName)s:%(lineno)d] %(levelname)s | %(message)s',
)
log = logging.getLogger(__name__)

with open('pyproject.toml', 'rb') as f:
    proj_info = tomllib.load(f)
VERSION = proj_info['project']['version']
VERSION_FULL = f"{proj_info['project']['name']} {proj_info['other']['version_full']}"
WEBSITE = proj_info['project']['urls']['Homepage']
