from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📍 Изменить локацию", callback_data="change_location")
    builder.button(text="📅 Выбрать расписание", callback_data="choose_schedule")
    builder.button(text="🗺️ Построить маршрут", callback_data="build_route")
    builder.button(text="⚙️ Настройки", callback_data="settings")
    builder.adjust(2)  # Одна кнопка в ряду
    return builder.as_markup()

