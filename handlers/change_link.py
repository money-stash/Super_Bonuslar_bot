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


class ChangeLink(StatesGroup):
    waiting_for_link = State()


def _load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(d: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


def _get_link(post: int) -> str | None:
    d = _load_data()
    return d.get(f"link_post{post}")


def _set_link(post: int, link: str):
    d = _load_data()
    d[f"link_post{post}"] = link
    _save_data(d)


def _cancel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Cancel", callback_data="cancel_change_link")]
        ]
    )


@router.callback_query(F.data.in_({"change_link_post1", "change_link_post2"}))
async def change_link_start(cb: CallbackQuery, state: FSMContext):
    post = 1 if cb.data.endswith("post1") else 2
    current = _get_link(post) or "—"
    await state.update_data(post=post)
    await cb.message.answer(
        f"Current link for post {post}:\n{current}\n\nSend a new link or press Cancel.",
        reply_markup=_cancel_kb(),
    )
    await state.set_state(ChangeLink.waiting_for_link)
    await cb.answer()


@router.message(ChangeLink.waiting_for_link, F.text)
async def change_link_save(msg: Message, state: FSMContext):
    data = await state.get_data()
    post = data.get("post")
    new_link = msg.text.strip()
    if not new_link:
        await msg.answer(
            "Empty link. Please send a new link or press Cancel.",
            reply_markup=_cancel_kb(),
        )
        return
    _set_link(post, new_link)
    await msg.answer(f"Link for post {post} has been updated:\n{new_link}")
    await state.clear()


@router.callback_query(F.data == "cancel_change_link")
async def change_link_cancel(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("Link change cancelled.")
    await cb.answer()


@router.message(F.text == "/cancel")
async def change_link_cancel_msg(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Cancelled.")
