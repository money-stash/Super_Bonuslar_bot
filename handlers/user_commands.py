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
from utils.json_utils import get_post1, get_post2
from config import DB_PATH

router = Router()

DATA_FILE = os.path.join("data", "data.json")


def load_next_post2_text() -> str:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("next_post2_text") or "➡️"


def kb_for_post1(p1, p2):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=p1["button_text"] or "↗️", url=p1["link"])],
            [InlineKeyboardButton(text=load_next_post2_text(), callback_data="post:2")],
        ]
    )


def kb_for_post2(p2):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=p2["button_text"] or "↗️", url=p2["link"])],
        ]
    )


@router.message(F.text == "/start")
async def start_func(msg: Message):
    user_id = msg.from_user.id
    await add_user_if_not_exists(DB_PATH, user_id)
    p1 = get_post1()
    p2 = get_post2()
    photo = FSInputFile("images/post1.jpeg")
    await msg.answer_photo(
        photo=photo,
        caption=p1["text"],
        parse_mode="HTML",
        reply_markup=kb_for_post1(p1, p2),
    )


@router.callback_query(F.data == "post:2")
async def show_post2(cb: CallbackQuery):
    p2 = get_post2()
    photo = FSInputFile("images/post2.jpeg")
    await cb.message.answer_photo(
        photo=photo,
        caption=p2["text"],
        parse_mode="HTML",
        reply_markup=kb_for_post2(p2),
    )
    await cb.answer()
