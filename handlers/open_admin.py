from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/admin")
async def admin_panel(msg: Message):
    if msg.from_user.id in ADMIN_ID:
        kb = [
            [
                InlineKeyboardButton(
                    text="Change post 1 img", callback_data="change_img_post1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Change post 1 link", callback_data="change_link_post1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Change post 1 text", callback_data="change_text_post1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Change post 2 img", callback_data="change_img_post2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Change post 2 link", callback_data="change_link_post2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Change post 2 text", callback_data="change_text_post2"
                )
            ],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await msg.answer("Admin panel", reply_markup=keyboard)
    else:
        await msg.answer("You are not authorized to access the admin panel.")
