import pickle
from typing import Any


async def catch_data(message: Any) -> list[Any]:
    inner_storage = []
    part = pickle.loads(message.body)
    if part not in inner_storage:
        inner_storage.append(part)
    print(inner_storage)
    return inner_storage
