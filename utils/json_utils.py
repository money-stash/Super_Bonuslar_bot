import json
import os

DATA_FILE = os.path.join("data", "data.json")


def get_post1() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "text": data.get("text_post1"),
        "link": data.get("link_post1"),
        "button_text": data.get("link_text1"),
    }


def get_post2() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "text": data.get("text_post2"),
        "link": data.get("link_post2"),
        "button_text": data.get("link_text2"),
        "next_post2_text": data.get("next_post2_text"),
    }
