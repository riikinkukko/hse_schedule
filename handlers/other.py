from aiogram import Router
from aiogram.types import Message

from keyboards import get_main_menu


other_router = Router(name=__name__)


@other_router.message()
async def unknown_message(message: Message):
    await message.answer(
        "Пожалуйста, используйте меню для навигации:",
        reply_markup=get_main_menu()
    )