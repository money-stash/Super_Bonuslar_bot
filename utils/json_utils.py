import json
import os

DATA_FILE = os.path.join("data", "data.json")


def load_data() -> dict:
    """Load all data from JSON file"""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_post_data(post_num: int) -> dict:
    """Get post data by post number (1-8)"""
    data = load_data()
    return {
        "text": data.get(f"text_post{post_num}", ""),
        "link": data.get(f"link_post{post_num}", ""),
        "button_text": data.get(f"link_text{post_num}", "🤑 Play Now! 🤑"),
        "next_text": data.get(f"next_post{post_num}_text", "Next Deal 👉"),
    }


# Backward compatibility - keep old function names
def get_post1() -> dict:
    """Get first post data (backward compatibility)"""
    return get_post_data(1)


def get_post2() -> dict:
    """Get second post data (backward compatibility)"""
    return get_post_data(2)


def get_all_posts() -> list:
    """Get all posts data as a list"""
    return [get_post_data(i) for i in range(1, 9)]


def get_post_count() -> int:
    """Get total number of posts available"""
    data = load_data()
    count = 0
    for i in range(1, 20):  # Check up to 20 posts
        if f"text_post{i}" in data:
            count = i
    return count
