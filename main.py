import asyncio
import logging
import bot_token
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Включаем логирование
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = bot_token.TELEGRAM_TOKEN

# Создаем экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Определяем состояния для FSM
class UserStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_schedule = State()
    main_menu = State()

# Создаем главное меню с кнопками
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📍 Изменить локацию", callback_data="change_location")
    builder.button(text="📅 Выбрать расписание", callback_data="choose_schedule")
    builder.button(text="🗺️ Построить маршрут", callback_data="build_route")
    builder.button(text="⚙️ Настройки", callback_data="settings")
    builder.adjust(2)  # Одна кнопка в ряду
    return builder.as_markup()

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    await message.answer(
        "Добро пожаловать в бот для построения маршрутов по расписанию! 🚀"
        "Выберите действие из меню ниже:",
        reply_markup=get_main_menu()
    )

# Обработчик команды /menu
@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )

# Обработчик кнопки "Изменить локацию"
@router.callback_query(F.data == "change_location")
async def change_location(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_location)
    await callback.message.edit_text(
        "Пожалуйста, отправьте вашу текущую локацию через вложение 📎 -> Location",
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    await callback.answer()

# Обработчик получения локации от пользователя
@router.message(UserStates.waiting_for_location, F.location)
async def location_received(message: Message, state: FSMContext):
    # Здесь будет интеграция с будущим модулем для сохранения локации
    latitude = message.location.latitude
    longitude = message.location.longitude
    
    # Сохраняем локацию в состоянии пользователя
    await state.update_data(user_location=(latitude, longitude))
    
    await state.set_state(UserStates.main_menu)
    await message.answer(
        f"Ваша локация сохранена: широта {latitude}, долгота {longitude}",
        reply_markup=get_main_menu()
    )

# Обработчик кнопки "Выбрать расписание"
@router.callback_query(F.data == "choose_schedule")
async def choose_schedule(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_schedule)
    
    # Здесь будет интеграция с будущим модулем для выбора расписания
    schedule_options = [
        "Расписание группы 1",
        "Расписание группы 2", 
        "Расписание преподавателя",
        "Индивидуальное расписание"
    ]
    
    builder = InlineKeyboardBuilder()
    for i, option in enumerate(schedule_options):
        builder.button(text=option, callback_data=f"schedule_{i}")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    
    await callback.message.edit_text(
        "Выберите тип расписания:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

# Обработчик выбора расписания
@router.callback_query(F.data.startswith("schedule_"))
async def schedule_selected(callback: CallbackQuery, state: FSMContext):
    schedule_index = int(callback.data.split("_")[1])
    schedule_names = [
        "Расписание группы 1",
        "Расписание группы 2", 
        "Расписание преподавателя",
        "Индивидуальное расписание"
    ]
    
    # Здесь будет интеграция с будущим модулем для сохранения выбранного расписания
    selected_schedule = schedule_names[schedule_index] if schedule_index < len(schedule_names) else "Неизвестное расписание"
    await state.update_data(user_schedule=selected_schedule)
    
    await state.set_state(UserStates.main_menu)
    await callback.message.edit_text(
        f"Вы выбрали: {selected_schedule}",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# Обработчик кнопки "Построить маршрут"
@router.callback_query(F.data == "build_route")
async def build_route(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    
    # Проверяем, есть ли у пользователя сохраненные данные
    location = user_data.get("user_location")
    schedule = user_data.get("user_schedule")
    
    if not location:
        await callback.message.edit_text(
            "Сначала установите вашу локацию!",
            reply_markup=get_main_menu()
        )
        await callback.answer()
        return
        
    if not schedule:
        await callback.message.edit_text(
            "Сначала выберите расписание!",
            reply_markup=get_main_menu()
        )
        await callback.answer()
        return
    
    # Здесь будет интеграция с будущими модулями:
    # 1. Модуль парсинга расписания
    # 2. Модуль построения маршрута
    # 3. Модуль работы с SQL
    
    await callback.message.edit_text(
        "🔄 Строим маршрут..."
        "Это может занять некоторое время.",
        reply_markup=None
    )
    
    # Имитация работы алгоритмов
    # parsed_schedule = parse_schedule(schedule)
    # route = build_route_algorithm(location, parsed_schedule)
    # save_to_db(user_id, route, schedule)
    
    # Для демонстрации просто покажем сообщение
    await callback.message.answer(
        "✅ Маршрут успешно построен!"
        "Ваш маршрут готов к использованию.",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# Обработчик кнопки "Настройки"
@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑️ Очистить данные", callback_data="clear_data")
    builder.button(text="📊 Статистика", callback_data="statistics")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    
    await callback.message.edit_text( "⚙️ Настройки:"
        "Выберите действие:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

# Обработчик кнопки "Очистить данные"
@router.callback_query(F.data == "clear_data")
async def clear_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🗑️ Все ваши данные очищены!",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# Обработчик кнопки "Статистика"
@router.callback_query(F.data == "statistics")
async def statistics(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    location = user_data.get("user_location")
    schedule = user_data.get("user_schedule")
    
    stats_text = "📊 Ваши настройки:"
    if location:
        stats_text += f"📍 Локация: установлена"
    else:
        stats_text += f"📍 Локация: не установлена"
        
    if schedule:
        stats_text += f"📅 Расписание: установлено"
    else:
        stats_text += f"📅 Расписание: не выбрано"
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=get_main_menu()
    )
    await callback.answer()

# Обработчик кнопки "Назад"
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# Обработчик непредвиденных сообщений
@router.message(UserStates.main_menu)
async def unknown_message(message: Message):
    await message.answer(
        "Пожалуйста, используйте меню для навигации:",
        reply_markup=get_main_menu()
    )

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())