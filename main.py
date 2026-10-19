import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai
import asyncio

# Xatoliklarni kuzatish uchun loglarni yoqamiz
logging.basicConfig(level=logging.INFO)

# Token va API kalit
BOT_TOKEN = "8969663199:AAGwb_3TnAypiBdR779ymjzmQe7lMJaKwYA"
GEMINI_API_KEY = "AQ.Ab8RN6Jzaf_Ns_Y-vCm3RuRe3o24dlKF5--LAoSeUDoCrCvIqg" 

# Sun'iy intellektni sozlash
genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash") 

# Botni ishga tushirish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start buyrug'i
@dp.message(Command("start"))
async def start_command(message: types.Message):
    welcome_text = (
        "👋 Assalomu alaykum! Men maktabingizning Sun'iy Intellekt yordamchisiman.\n\n"
        "🤖 Menga dars konspektlari, testlar tuzish, insholar yozish yoki istalgan faningizdan "
        "savollar bo'yicha murojaat qilishingiz mumkin. Savolingizni yozib yuboring!"
    )
    await message.answer(welcome_text)

# Sun'iy Intellekt javobi
@dp.message(F.text)
async def handle_ai_request(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        prompt = f"Sen maktab o'quvchilari va o'qituvchilariga yordam beradigan samimiy AI yordamchisan. Savol: {message.text}"
        response = ai_model.generate_content(prompt)
        await message.answer(response.text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("⚠️ Javob tayyorlashda xatolik bo'ldi. Birozdan so'ng qayta urunib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
