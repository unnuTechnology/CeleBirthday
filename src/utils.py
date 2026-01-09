import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s | %(module)s.%(funcName)s:%(lineno)d] %(levelname)s | %(message)s',
)
log = logging.getLogger(__name__)
