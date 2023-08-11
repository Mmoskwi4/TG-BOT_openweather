"""Телеграмм-бот, который выводит небольшую сводку погоды по запрашиваемому городу"""

import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from transliterate import translit

# Объект бота
tg_bot_token = ''
bot = Bot(token=tg_bot_token)
# Объект weather
open_weather_token = ''
# Диспетчер
dp = Dispatcher(bot)

# Начало работы с ботом. Ответ после команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\nНапиши мне название \U0001F303города\U0001F303"
                         f"\nЯ пришлю тебе сводку погоды!", parse_mode='Markdown')


@dp.message_handler()
async def get_weather(message: types.Message):
    # Коды смайликов
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    # Процесс работы состоит из передачи запроса на openweathermap и вывода сообщения. Ответ сохраняется в json'е и мы выделяем необходимые данные.
    try:
        text = translit(message.text, reversed=True)
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***")

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)