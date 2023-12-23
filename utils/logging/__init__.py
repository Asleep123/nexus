import logging
import sys
import os

root = logging.getLogger("uptime")
root.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename="uptime.log", encoding="utf-8", mode="w")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

root.addHandler(handler)

with open("../uptime.log", "w") as _f:
    pass

sys.path.append("../uptime.log")

uptimelog = logging.getLogger("uptime")

def log(msg: str) -> None:
    uptimelog.info(msg)

def warn(msg: str) -> None:
    uptimelog.error(msg)