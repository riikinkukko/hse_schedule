from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards import get_main_menu


command_router = Router(name=__name__)


@command_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в бот для построения маршрутов по расписанию! 🚀"
        "Выберите действие из меню ниже:",
        reply_markup=get_main_menu()
    )

@command_router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )