import re
from typing import Final

PATTERN: Final[re.Pattern[str]] = re.compile(r"§[0-9a-fklmnorx]")


def remove_minecraft_colors(text: str) -> str:
    return PATTERN.sub("", text)
