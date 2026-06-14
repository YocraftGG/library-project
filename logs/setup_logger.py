import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler = logging.FileHandler("logs/app.log", encoding="utf-8")

handler.setFormatter(formatter)
logger.addHandler(handler)