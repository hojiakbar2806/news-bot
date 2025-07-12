import json
import os
from pathlib import Path

CACHE_PATH = Path("cache/chats.json")


def save_chat_id(chat_id: int):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    if chat_id not in data:
        data.append(chat_id)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def get_chat_ids() -> list[int]:
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def delete_chat_id(chat_id: int):
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if chat_id in data:
            data.remove(chat_id)
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
