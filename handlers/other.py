from aiogram import Router
from aiogram.types import Message

from keyboards import get_main_menu
from lexicon import LEXICON_MESSAGES


other_router = Router(name=__name__)


@other_router.message()
async def unknown_message(message: Message):
    await message.answer(
        text=LEXICON_MESSAGES["unknown_message"],
        reply_markup=get_main_menu()
    )