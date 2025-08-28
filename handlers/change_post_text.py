from aiogram import F, Router
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import json
import os

DATA_FILE = os.path.join("data", "data.json")
router = Router()


class ChangeText(StatesGroup):
    waiting_for_text = State()


def _load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(d: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


def _get_text(post: int) -> str | None:
    d = _load_data()
    return d.get(f"text_post{post}")


def _set_text(post: int, text_html: str):
    d = _load_data()
    d[f"text_post{post}"] = text_html
    _save_data(d)


def _cancel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Cancel", callback_data="cancel_change_text")]
        ]
    )


@router.callback_query(F.data.in_({"change_text_post1", "change_text_post2"}))
async def change_text_start(cb: CallbackQuery, state: FSMContext):
    post = 1 if cb.data.endswith("post1") else 2
    current = _get_text(post) or "—"
    await state.update_data(post=post)
    await cb.message.answer(
        f"Current text for post {post}:\n\n{current}\n\nSend a new text (HTML formatting is supported) or press Cancel.",
        parse_mode="HTML",
        reply_markup=_cancel_kb(),
    )
    await state.set_state(ChangeText.waiting_for_text)
    await cb.answer()


@router.message(ChangeText.waiting_for_text, F.text)
async def change_text_save(msg: Message, state: FSMContext):
    data = await state.get_data()
    post = data.get("post")
    new_text_html = msg.html_text or msg.text or ""
    if not new_text_html.strip():
        await msg.answer(
            "Empty text. Please send a new text or press Cancel.",
            reply_markup=_cancel_kb(),
        )
        return
    _set_text(post, new_text_html)
    await msg.answer(f"Text for post {post} has been updated.", reply_markup=None)
    await msg.answer(new_text_html, parse_mode="HTML")
    await state.clear()


@router.callback_query(F.data == "cancel_change_text")
async def change_text_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("Text change cancelled.")
    await cb.answer()


@router.message(F.text == "/cancel")
async def change_text_cancel_msg(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Cancelled.")
