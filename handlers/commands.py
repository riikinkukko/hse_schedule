from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards import get_main_menu
from states import UserStates
from database.database import db

command_router = Router(name=__name__)


@command_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if db.user_exists(user_id):
        user_groups = db.get_user_groups(user_id)
        if user_groups:
            group_cst, group_eng = user_groups
            await message.answer(
                f"👋 С возвращением!\n"
                f"📊 Ваши настройки:\n"
                f"• Группа КНТ: {group_cst}\n"
                f"• Группа английского: {group_eng}\n\n"
                f"Выберите действие:",
                reply_markup=get_main_menu()
            )
            await state.set_state(UserStates.main_menu)
        else:
            await message.answer(
                "❌ Произошла ошибка при загрузке ваших данных. "
                "Пожалуйста, пройдите регистрацию заново.",
                reply_markup=get_main_menu()
            )
    else:
        await message.answer(
            "👋 Добро пожаловать в бот расписания НИУ ВШЭ!\n\n"
            "Для начала работы мне нужно узнать ваши группы.\n"
            "📝 Введите вашу группу КНТ (только цифру, 1-7)"
        )
        await state.set_state(UserStates.waiting_for_cst_group)


@command_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if not db.user_exists(user_id):
        await message.answer(
            "❌ Вы не зарегистрированы. Используйте /start для регистрации."
        )
        return

    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await state.set_state(UserStates.main_menu)


@command_router.message(Command("profile"))
async def cmd_profile(message: Message):
    user_id = message.from_user.id

    if not db.user_exists(user_id):
        await message.answer("❌ Вы не зарегистрированы. Используйте /start для регистрации.")
        return

    user_groups = db.get_user_groups(user_id)
    if user_groups:
        group_cst, group_eng = user_groups
        await message.answer(
            f"👤 Ваш профиль:\n"
            f"🆔 ID: {user_id}\n"
            f"📊 Группа КНТ: {group_cst}\n"
            f"🌍 Группа английского: {group_eng}"
        )
    else:
        await message.answer("❌ Не удалось загрузить данные профиля.")


@command_router.message(Command("reset"))
async def cmd_reset(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if db.user_exists(user_id):
        db.delete_user(user_id)

    await state.clear()
    await message.answer(
        "🗑️ Все ваши данные сброшены. Используйте /start для повторной регистрации."
    )


@command_router.message(Command("settings"))
async def cmd_settings(message: Message):
    user_id = message.from_user.id

    if not db.user_exists(user_id):
        await message.answer("❌ Вы не зарегистрированы. Используйте /start для регистрации.")
        return

    user_groups = db.get_user_groups(user_id)
    if user_groups:
        group_cst, group_eng = user_groups
        settings_text = (
            "⚙️ Настройки:\n\n"
            f"📊 Текущие настройки:\n"
            f"• Группа КНТ: {group_cst}\n"
            f"• Группа английского: {group_eng}\n\n"
            "Выберите действие:"
        )
    else:
        settings_text = "⚙️ Настройки:\n\nВыберите действие:"

    from keyboards import get_settings_menu
    await message.answer(settings_text, reply_markup=get_settings_menu())