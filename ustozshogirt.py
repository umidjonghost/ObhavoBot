import asyncio
import requests
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

bot = Bot(token="7833049537:AAHtbhkBD9rdSQ4aFIUB0YHi_0cDhQ8BsBs")
dp = Dispatcher()
WEATHER_API_KEY = "b80278028123a6bbdee646095d3a8400"




def get_weather_by_coords(latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city = data["name"]
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return f"📍 **Sizning joylashuvingiz bo‘yicha ob-havo ma’lumoti ({city}):**\n" \
               f"🌡 **Harorat:** {temp}°C\n" \
               f"🌦 **Holat:** {weather.capitalize()}\n" \
               f"💧 **Namlik:** {humidity}%\n" \
               f"🌬 **Shamol tezligi:** {wind_speed} m/s"
    else:
        return "❌ Ob-havo ma'lumotlarini olishda xatolik yuz berdi."


# 🔹 /location komandasi (lokatsiya so‘rash)
@dp.message(Command("location"))
async def request_location(message: Message):
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "📍 Iltimos, quyidagi tugma orqali **joylashuvingizni yuboring** va biz sizga aniq ob-havo ma’lumotlarini taqdim etamiz.",
        reply_markup=location_keyboard
    )


# 🔹 Foydalanuvchi joylashuv yuborganida ishlaydigan funksiya
@dp.message(F.location)
async def get_weather_from_location(message: Message):
    latitude = message.location.latitude  # Kenglik (lat)
    longitude = message.location.longitude  # Uzunlik (lon)

    weather_info = get_weather_by_coords(latitude, longitude)

    await message.answer(weather_info, reply_markup=ReplyKeyboardRemove())  # Tugmalarni o‘chirish


@dp.message(Command("help"))
async def catch_command(message:Message):
    await message.answer(text="""📌 Yordam Bo‘limi ℹ️

👋 Assalomu alaykum! Ushbu bot sizga istalgan shahar ob-havo ma’lumotlarini taqdim etadi. Foydalanish bo‘yicha qisqacha qo‘llanma:

🔹 Shahar bo‘yicha ob-havo olish
📍 Shunchaki shahar nomini tanlang yoki yozing. Masalan: Toshkent, Samarqand, Farg‘ona.

🔹 Joylashuv bo‘yicha ob-havo
📌 /location buyrug‘ini yuboring va bot sizning joriy joylashuvingiz asosida ob-havo ma’lumotlarini ko‘rsatadi.

🔹 7 kunlik ob-havo bashorati
📅 /week buyrug‘idan foydalaning va tanlangan shahar uchun haftalik ob-havo prognozini oling.

🔹 Qo‘shimcha imkoniyatlar
💡 Agar sizda taklif yoki savollaringiz bo‘lsa, biz bilan bog‘laning.

🚀 Botdan unumli foydalaning va doimo ob-havodan xabardor bo‘ling! 😊""")

@dp.message(Command("start"))
async def catch_command(message: Message):
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍Farg'ona"), KeyboardButton(text='📍Toshkent')],
            [KeyboardButton(text='📍Namangan'),KeyboardButton(text='📍Qoqon')],
            [KeyboardButton(text="📍Xorazm"), KeyboardButton(text='📍Samarqand')],
            [KeyboardButton(text='📍Andijon'), KeyboardButton(text='📍Nukus')],
            [KeyboardButton(text="📍Qarshi"), KeyboardButton(text='📍Olmaliq')],
            [KeyboardButton(text='📍Navoiy'),     KeyboardButton(text='Exit')]
        ], resize_keyboard=True
    )
    await message.answer(text=f"""📍🌍 Ob-havo Botiga Xush Kelibsiz! ☀️🌧

👋 Assalomu alaykum, do‘st! Men sizga istalgan shahar ob-havo ma’lumotlarini taqdim qiluvchi yordamchingizman. 🌎✨

📍 Foydalanish qoidalari:
🔹 Shahar nomini tanlang (masalan: Toshkent yoki Qo'qon).
🔹 Ob-havo ma’lumotlarini oling: harorat, namlik, shamol tezligi va boshqalar.

💡 Qo‘shimcha buyruqlar:
📅 /week – 7 kunlik ob-havo bashorati
📌 /location – Joriy joylashuv bo‘yicha ob-havo
ℹ️ /help – Qo‘llanma

📝 Hoziroq shahar nomini kiriting va ob-havoni bilib oling! 🌤✨""", reply_markup=reply_keyboard)


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return f"🌍 {city} shahrining ob-havo ma’lumoti:\n" \
               f"🌡 Harorat: {temp}°C\n" \
               f"🌦 Holat: {weather.capitalize()}\n" \
               f"💧 Namlik: {humidity}%\n" \
               f"🌬 Shamol tezligi: {wind_speed} m/s"
    else:
        return "❌ Ob-havo ma'lumotlarini olishda xatolik yuz berdi."


@dp.message(F.text.startswith("📍"))
async def send_weather(message: Message):
    city = message.text.replace("📍", "").strip()
    weather_info = get_weather(city)
    await message.answer(weather_info)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())