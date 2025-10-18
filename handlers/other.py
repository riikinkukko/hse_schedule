from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import get_main_menu
from states import UserStates
from database.database import db

other_router = Router(name=__name__)


@other_router.message(UserStates.waiting_for_cst_group)
async def process_cst_group(message: Message, state: FSMContext):
    try:
        group_cst = int(message.text.strip())

        if 1 <= group_cst <= 10:
            await state.update_data(group_cst=group_cst)
            await message.answer(
                f"✅ Группа КНТ: {group_cst}\n\n"
                f"📝 Теперь введите вашу группу по английскому языку (только цифру, например: 3):"
            )
            await state.set_state(UserStates.waiting_for_eng_group)
        else:
            await message.answer(
                "❌ Пожалуйста, введите корректный номер группы КНТ (от 1 до 10):"
            )
    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите только цифру (например: 5):"
        )


@other_router.message(UserStates.waiting_for_eng_group)
async def process_eng_group(message: Message, state: FSMContext):
    try:
        group_eng = int(message.text.strip())

        if 1 <= group_eng <= 10:
            user_data = await state.get_data()
            group_cst = user_data.get('group_cst')
            user_id = message.from_user.id

            if db.add_user(user_id, group_cst, group_eng):
                await message.answer(
                    f"✅ Регистрация завершена!\n\n"
                    f"📊 Ваши настройки:\n"
                    f"• Группа КНТ: {group_cst}\n"
                    f"• Группа английского: {group_eng}\n\n"
                    f"Теперь вы можете пользоваться всеми функциями бота!",
                    reply_markup=get_main_menu()
                )
                await state.set_state(UserStates.main_menu)
            else:
                await message.answer(
                    "❌ Произошла ошибка при сохранении данных. Попробуйте снова: /start"
                )
        else:
            await message.answer(
                "❌ Пожалуйста, введите корректный номер группы английского (от 1 до 10):"
            )
    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите только цифру (например: 3):"
        )


@other_router.message()
async def other_messages(message: Message):
    await message.answer("Неизвестная команда. Используйте /start для начала работы.")