from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from keyboards import get_main_menu
from states import UserStates
from parsers.excel_parser import fetch_schedule

menu_router = Router(name=__name__)


@menu_router.callback_query(F.data == "choose_schedule")
async def choose_schedule(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_for_schedule)

    schedule_options = [
        "📅 Получить расписание на сегодня",
        "📅 Получить расписание на завтра",
        "📅 Получить полное расписание",
        "🔍 Поиск по предмету",
    ]

    builder = InlineKeyboardBuilder()
    for i, option in enumerate(schedule_options):
        builder.button(text=option, callback_data=f"schedule_{i}")
    builder.button(text="⬅️ Назад", callback_data="back_to_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        "Выберите действие с расписанием:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@menu_router.callback_query(F.data.startswith("schedule_"))
async def schedule_selected(callback: CallbackQuery, state: FSMContext):
    schedule_index = int(callback.data.split("_")[1])

    if schedule_index == 0:
        await get_today_schedule(callback, state)
    elif schedule_index == 1:
        await get_tomorrow_schedule(callback, state)
    elif schedule_index == 2:
        await get_full_schedule(callback, state)
    elif schedule_index == 3:
        await search_subject(callback, state)


async def get_today_schedule(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📥 Загружаю расписание на сегодня...")

    schedule_data = await fetch_schedule()

    if not schedule_data:
        await callback.message.edit_text(
            "❌ Не удалось загрузить расписание. Попробуйте позже.",
            reply_markup=get_main_menu()
        )
        return

    import datetime
    days_mapping = {
        0: 'mon',
        1: 'tue',
        2: 'wed',
        3: 'thu',
        4: 'fri',
        5: 'sat',
    }

    today_index = datetime.datetime.today().weekday()
    today_key = days_mapping.get(today_index, 'mon')

    today_lessons = schedule_data.get(today_key, [])
    formatted_schedule = format_daily_schedule(today_lessons, get_day_name(today_key))

    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Полное расписание", callback_data="schedule_2")
    builder.button(text="⬅️ Назад", callback_data="choose_schedule")
    builder.adjust(1)

    await callback.message.edit_text(
        formatted_schedule,
        reply_markup=builder.as_markup()
    )


async def get_tomorrow_schedule(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📥 Загружаю расписание на завтра...")

    schedule_data = await fetch_schedule()

    if not schedule_data:
        await callback.message.edit_text(
            "❌ Не удалось загрузить расписание. Попробуйте позже.",
            reply_markup=get_main_menu()
        )
        return

    import datetime
    days_mapping = {
        0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat',
    }

    tomorrow_index = (datetime.datetime.today().weekday() + 1) % 6
    tomorrow_key = days_mapping.get(tomorrow_index, 'mon')

    tomorrow_lessons = schedule_data.get(tomorrow_key, [])
    formatted_schedule = format_daily_schedule(tomorrow_lessons, get_day_name(tomorrow_key))

    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Полное расписание", callback_data="schedule_2")
    builder.button(text="⬅️ Назад", callback_data="choose_schedule")
    builder.adjust(1)

    await callback.message.edit_text(
        formatted_schedule,
        reply_markup=builder.as_markup()
    )


async def get_full_schedule(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📥 Загружаю полное расписание...")

    schedule_data = await fetch_schedule()

    if not schedule_data:
        await callback.message.edit_text(
            "❌ Не удалось загрузить расписание. Попробуйте позже.",
            reply_markup=get_main_menu()
        )
        return

    formatted_schedule = format_weekly_schedule(schedule_data)

    builder = InlineKeyboardBuilder()
    builder.button(text="📅 На сегодня", callback_data="schedule_0")
    builder.button(text="📅 На завтра", callback_data="schedule_1")
    builder.button(text="⬅️ Назад", callback_data="choose_schedule")
    builder.adjust(1)

    await callback.message.edit_text(
        formatted_schedule,
        reply_markup=builder.as_markup()
    )


async def search_subject(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("🔍 Введите название предмета для поиска:")
    await state.set_state(UserStates.waiting_for_subject_search)


@menu_router.message(UserStates.waiting_for_subject_search)
async def process_subject_search(message: Message, state: FSMContext):
    subject_name = message.text.strip().lower()

    await message.answer(f"🔍 Ищу предмет '{message.text}'...")

    schedule_data = await fetch_schedule()

    if not schedule_data:
        await message.answer(
            "❌ Не удалось загрузить расписание. Попробуйте позже.",
            reply_markup=get_main_menu()
        )
        await state.clear()
        return

    found_lessons = search_lessons_by_name(schedule_data, subject_name)

    if found_lessons:
        response = f"🔍 Найдены занятия по '{message.text}':\n\n"
        for lesson_info in found_lessons:
            response += f"📅 {lesson_info['day']}, {lesson_info['time']} пара\n"
            if isinstance(lesson_info['lesson'], dict):
                response += f"   👨‍🏫 {lesson_info['lesson'].get('teacher', 'Не указан')}\n"
                response += f"   🏫 {lesson_info['lesson'].get('classnumber', 'Не указана')}\n"
            response += "\n"
    else:
        response = f"❌ Занятия по '{message.text}' не найдены в расписании."

    await message.answer(response, reply_markup=get_main_menu())
    await state.clear()


def format_daily_schedule(lessons, day_name):
    result = [f"📅 {day_name}:\n"]

    for i, lesson in enumerate(lessons, 1):
        result.append(f"{i}. {format_lesson(lesson)}")

    if not any(lesson != 'None' for lesson in lessons):
        result.append("\n🎉 Выходной! Занятий нет.")

    return "\n".join(result)


def format_weekly_schedule(schedule_data):
    result = ["📊 Полное расписание на неделю:\n"]

    days_order = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    day_names = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота'
    }

    for day_key in days_order:
        day_name = day_names[day_key]
        lessons = schedule_data.get(day_key, [])

        result.append(f"\n📅 {day_name}:")

        has_lessons = False
        for i, lesson in enumerate(lessons, 1):
            if lesson != 'None':
                result.append(f"  {i}. {format_lesson(lesson)}")
                has_lessons = True

        if not has_lessons:
            result.append("  🎉 Выходной!")

    return "\n".join(result)


def format_lesson(lesson):
    if lesson == 'None':
        return "-"

    if isinstance(lesson, list):
        english_lessons = []
        for eng_lesson in lesson:
            if eng_lesson.get('group') == 8:
                class_info = f"ауд. {eng_lesson['classnumber']}" if eng_lesson['classnumber'] != 'online' else "онлайн"
                return f"🇬🇧 {eng_lesson['lesson_name']} ({class_info}) - {eng_lesson['teacher']}"
        return "Английский язык (группа не указана)"

    else:
        class_info = f"ауд. {lesson['classnumber']}" if lesson['classnumber'] != 'online' else "онлайн"
        return f"{lesson['lesson_name']} ({class_info}) - {lesson['teacher']}"


def get_day_name(day_key):
    day_names = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота'
    }
    return day_names.get(day_key, 'Неизвестный день')


def search_lessons_by_name(schedule_data, subject_name):
    found_lessons = []
    days_order = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    day_names = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота'
    }

    for day_key in days_order:
        day_name = day_names[day_key]
        lessons = schedule_data.get(day_key, [])

        for i, lesson in enumerate(lessons, 1):
            if lesson != 'None':
                lesson_name = ""

                if isinstance(lesson, list):
                    for eng_lesson in lesson:
                        if eng_lesson.get('group') == 5:
                            lesson_name = eng_lesson['lesson_name'].lower()
                            break
                else:
                    lesson_name = lesson['lesson_name'].lower()

                if subject_name in lesson_name:
                    found_lessons.append({
                        'day': day_name,
                        'time': i,
                        'lesson': lesson
                    })

    return found_lessons


# Остальные хендлеры остаются без изменений
@menu_router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑️ Очистить данные", callback_data="clear_data")
    builder.button(text="📊 Статистика", callback_data="statistics")
    builder.button(text="🔄 Обновить расписание", callback_data="update_schedule")
    builder.button(text="⬅️ Назад", callback_data="back_to_menu")
    builder.adjust(1)

    await callback.message.edit_text(
        "⚙️ Настройки:\n"
        "Выберите действие:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@menu_router.callback_query(F.data == "update_schedule")
async def update_schedule(callback: CallbackQuery):

    await callback.message.edit_text("🔄 Обновляю расписание...")

    schedule_data = await fetch_schedule()

    if schedule_data:
        await callback.message.edit_text(
            "✅ Расписание успешно обновлено!",
            reply_markup=get_main_menu()
        )
    else:
        await callback.message.edit_text(
            "❌ Не удалось обновить расписание. Попробуйте позже.",
            reply_markup=get_main_menu()
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