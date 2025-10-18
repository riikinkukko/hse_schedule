from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext


from keyboards import get_main_menu
from states import UserStates


menu_router = Router(name=__name__)


@menu_router.callback_query(F.data == "choose_schedule")
async def choose_schedule(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_schedule)
    
    schedule_options = [
        "Расписание группы КНТ1",
        "Расписание группы КНТ2", 
        "Расписание группы КНТ3", 
        "Расписание группы КНТ4",
        "Расписание группы КНТ5", 
        "Расписание группы КНТ6",    
        "Расписание группы КНТ7",
    ]
    
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(schedule_options):
        builder.button(text=option, callback_data=f"schedule_{i}")
    builder.button(text="⬅️ Назад", callback_data="back_to_menu")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Выберите тип расписания:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@menu_router.callback_query(F.data.startswith("schedule_"))
async def schedule_selected(callback: CallbackQuery, state: FSMContext):
    schedule_index = int(callback.data.split("_")[1])
    schedule_names = [
        "Расписание группы КНТ1",
        "Расписание группы КНТ2", 
        "Расписание группы КНТ3", 
        "Расписание группы КНТ4",
        "Расписание группы КНТ5", 
        "Расписание группы КНТ6",    
        "Расписание группы КНТ7",    
        ]
    
    selected_schedule = schedule_names[schedule_index] if schedule_index < len(schedule_names) else "Неизвестное расписание"
    await state.update_data(user_schedule=selected_schedule)
    await state.set_state(UserStates.main_menu)
    
    await callback.message.edit_text(
        f"✅ Вы выбрали: {selected_schedule}",
        reply_markup=get_main_menu()
    )
    await callback.answer()


@menu_router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑️ Очистить данные", callback_data="clear_data")
    builder.button(text="📊 Статистика", callback_data="statistics")
    builder.button(text="⬅️ Назад", callback_data="back_to_menu")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "⚙️ Настройки:\n"
        "Выберите действие:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@menu_router.callback_query(F.data == "clear_data")
async def clear_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🗑️ Все ваши данные очищены!",
        reply_markup=get_main_menu()
    )
    await callback.answer()


@menu_router.callback_query(F.data == "statistics")
async def statistics(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    schedule = user_data.get("user_schedule")
    
    stats_text = "📊 Ваши настройки:\n"
        
    if schedule:
        stats_text += f"📅 Расписание: {schedule}\n"
    else:
        stats_text += f"📅 Расписание: не выбрано\n"
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=get_main_menu()
    )
    await callback.answer()


@menu_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu()
    )