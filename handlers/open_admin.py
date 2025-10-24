from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/admin")
async def admin_panel(msg: Message):
    if msg.from_user.id not in ADMIN_ID:
        return await msg.answer("You are not authorized to access the admin panel.")

    buttons = []
    for i in range(1, 3):
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text=f"Change post {i} img", callback_data=f"change_img_post{i}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Change post {i} link",
                        callback_data=f"change_link_post{i}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Change post {i} text",
                        callback_data=f"change_text_post{i}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Change post {i} link text",
                        callback_data=f"change_link_text_post{i}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"Change next post {i} text",
                        callback_data=f"change_next_post_text_post{i}",
                    )
                ],
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer("Admin panel", reply_markup=keyboard)
