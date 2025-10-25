from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    FSInputFile,
)
import json
import os
from data.database import add_user_if_not_exists
from utils.json_utils import get_post_data
from config import DB_PATH

router = Router()
DATA_FILE = os.path.join("data", "data.json")


def load_data() -> dict:
    """Load all data from JSON file"""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_post_by_number(post_num: int) -> dict:
    """Get post data by post number (1-10)"""
    data = load_data()
    return {
        "text": data.get(f"text_post{post_num}", ""),
        "link": data.get(f"link_post{post_num}", ""),
        "button_text": data.get(f"link_text{post_num}", "🤑 Play Now! 🤑"),
        "next_text": data.get(f"next_post{post_num}_text", "Next Deal 👉"),
    }


def kb_for_post(post_num: int, total_posts: int = 2):
    """Generate keyboard for any post number"""
    post_data = get_post_by_number(post_num)
    keyboard = []

    # Add main action button
    if post_data["link"]:
        keyboard.append(
            [InlineKeyboardButton(text=post_data["button_text"], url=post_data["link"])]
        )

    # Add next button (if not last post)
    if post_num < total_posts:
        next_text = post_data["next_text"]
        keyboard.append(
            [InlineKeyboardButton(text=next_text, callback_data=f"post:{post_num+1}")]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(F.text == "/start")
async def start_func(msg: Message):
    """Start command - show first post"""
    user_id = msg.from_user.id
    await add_user_if_not_exists(DB_PATH, user_id)

    post_data = get_post_by_number(1)
    photo = FSInputFile("images/post1.jpeg")

    await msg.answer_photo(
        photo=photo,
        caption=post_data["text"],
        parse_mode="HTML",
        reply_markup=kb_for_post(1),
    )


@router.callback_query(F.data.startswith("post:"))
async def show_post(cb: CallbackQuery):
    """Handle post navigation"""
    try:
        post_num = int(cb.data.split(":")[1])

        if post_num < 1 or post_num > 10:
            await cb.answer("Invalid post number", show_alert=True)
            return

        post_data = get_post_by_number(post_num)
        image_path = f"images/post{post_num}.jpeg"
        if not os.path.exists(image_path):
            await cb.message.answer(
                post_data.get("text", "📢 Post content is unavailable."),
                parse_mode="HTML",
                reply_markup=kb_for_post(post_num),
            )
            await cb.answer("Image not found, showing text instead.", show_alert=True)
            return

        photo = FSInputFile(image_path)

        await cb.message.answer_photo(
            photo=photo,
            caption=post_data.get("text", ""),
            parse_mode="HTML",
            reply_markup=kb_for_post(post_num),
        )

        await cb.answer()

    except (ValueError, IndexError) as e:
        await cb.answer("Error processing request", show_alert=True)
    except FileNotFoundError:
        await cb.message.answer(
            post_data.get("text", "📢 Post content is unavailable."),
            parse_mode="HTML",
            reply_markup=kb_for_post(post_num),
        )
        await cb.answer("Image file missing.", show_alert=True)
    except Exception as e:
        await cb.answer("Error processing request", show_alert=True)


# Alternative: Menu-style navigation
@router.message(F.text == "/menu")
async def show_menu(msg: Message):
    """Show menu with all posts"""
    keyboard = []

    # Create 2 columns of post buttons
    for i in range(0, 10, 2):
        row = []
        for j in range(2):
            if i + j < 10:
                post_num = i + j + 1
                row.append(
                    InlineKeyboardButton(
                        text=f"Post {post_num}", callback_data=f"post:{post_num}"
                    )
                )
        keyboard.append(row)

    await msg.answer(
        "📋 Choose a post to view:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
