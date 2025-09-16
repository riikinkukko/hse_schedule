import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
import token

TELEGRAM_TOKEN = token.TELEGRAM_TOKEN
YANDEX_API_KEY = token.YANDEX_API_KEY

DESTINATION = [37.620795, 55.753930]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Отправить локацию", request_location=True)
    kb.add(button)
    await message.answer("Привет! Отправь мне свою геолокацию, и я построю маршрут", reply_markup=kb)


@dp.message_handler(content_types=["location"])
async def handle_location(message: types.Message):
    user_loc = message.location
    origin = [user_loc.longitude, user_loc.latitude]

    url = "https://api.routing.yandex.net/v2/route"
    params = {
        "apikey": YANDEX_API_KEY,
        "waypoints": f"{origin[0]},{origin[1]}|{DESTINATION[0]},{DESTINATION[1]}",
        "mode": "driving",
        "lang": "ru_RU"
    }

    response = requests.get(url, params=params).json()

    if "routes" in response and response["routes"]:
        route = response["routes"][0]
        leg = route["legs"][0]

        distance = leg["length"]["text"]
        duration = leg["duration"]["text"]

        steps = []
        for step in leg["steps"]:
            if "instruction" in step:
                steps.append(step["instruction"]["text"])

        steps_text = "\n".join([f"➡ {s}" for s in steps])

        text = (
            f"Маршрут найден!\n\n"
            f"Расстояние: {distance}\n"
            f"Время в пути: {duration}\n\n"
            f"Шаги:\n{steps_text}"
        )
    else:
        text = "Не удалось построить маршрут"

    await message.answer(text, parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
