import re
from typing import Any


async def convert_to_uuid(text: str | Any) -> str:
    return re.sub(r"[^a-fA-F0-9-]", "", text)
