from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Получить расписание", callback_data="choose_schedule")
    builder.button(text="⚙️ Настройки", callback_data="settings")
    builder.adjust(1)
    return builder.as_markup()

def get_settings_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Изменить группу КНТ", callback_data="change_cst_group")
    builder.button(text="🌍 Изменить группу английского", callback_data="change_eng_group")
    builder.button(text="🗑️ Очистить данные", callback_data="clear_data")
    builder.button(text="📊 Статистика", callback_data="statistics")
    builder.button(text="⬅️ Назад", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()

def get_back_to_settings_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад в настройки", callback_data="settings")
    return builder.as_markup()