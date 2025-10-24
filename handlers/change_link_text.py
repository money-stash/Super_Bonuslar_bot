from aiogram import Router, F
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

router = Router()
DATA_FILE = os.path.join("data", "data.json")


class ChangeLinkText(StatesGroup):
    waiting_for_text = State()


def _ensure_data_dir():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def _load_data() -> dict:
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_data(data: dict):
    _ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_link_text(post: int) -> str | None:
    data = _load_data()
    return data.get(f"link_text{post}")


def _set_link_text(post: int, new_text: str):
    data = _load_data()
    data[f"link_text{post}"] = new_text
    _save_data(data)


def _cancel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Cancel", callback_data="cancel_change_link_text"
                )
            ]
        ]
    )


@router.callback_query(F.data.startswith("change_link_text_post"))
async def change_link_text_start(cb: CallbackQuery, state: FSMContext):
    try:
        post = int(cb.data.split("post")[-1])
    except Exception:
        await cb.answer("Invalid post id", show_alert=True)
        return
    current = _get_link_text(post) or "—"
    await state.update_data(post=post)
    await cb.message.answer(
        f"Current link text for post {post}:\n{current}\n\nSend a new link text or press Cancel.",
        reply_markup=_cancel_kb(),
    )
    await state.set_state(ChangeLinkText.waiting_for_text)
    await cb.answer()


@router.message(ChangeLinkText.waiting_for_text, F.text)
async def change_link_text_save(msg: Message, state: FSMContext):
    data = await state.get_data()
    post = data.get("post")
    if post is None:
        await msg.answer("Something went wrong. Please try again.")
        await state.clear()
        return
    new_text = msg.text.strip()
    if not new_text:
        await msg.answer(
            "Empty text. Please send a new link text or press Cancel.",
            reply_markup=_cancel_kb(),
        )
        return
    try:
        _set_link_text(post, new_text)
    except Exception as e:
        await msg.answer(f"Failed to save link text: {e}")
        await state.clear()
        return
    await msg.answer(f"Link text for post {post} has been updated:\n{new_text}")
    await state.clear()


@router.callback_query(F.data == "cancel_change_link_text")
async def change_link_text_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("Link text change cancelled.")
    await cb.answer()


@router.message(F.text == "/cancel")
async def change_any_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Cancelled.")
