import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""Ты — помощник, который переводит обычный текст в официальный деловой или юридический стиль.

Твоя задача: сохранить смысл сообщения, но переписать его грамотным официальным языком. Убрать разговорные выражения, сленг, эмоции. Добавить формальные обороты, вежливые формулировки и правильную структуру.

Правила:
— Не меняй суть и факты, только стиль.
— Не добавляй информацию, которой нет в оригинале.
— Если текст уже официальный — скажи об этом и предложи улучшения.
— Отвечай только переведённым текстом, без пояснений и комментариев.
— Если пользователь написал тип документа (жалоба, заявление, письмо) — учитывай это при переводе.
— Если тип не указан — переводи в нейтральный деловой стиль.

Формат ответа:
Просто переведённый текст. Никаких заголовков, пояснений или «вот ваш текст:»."""
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

WELCOME_TEXT = """Привет! Я помогаю писать официальные письма, жалобы и заявления.

Просто напиши мне своё сообщение как умеешь — я переведу его в официальный язык.

Например:
_«хочу вернуть деньги за телефон, он сломался через неделю»_

Попробуй — отправь любой текст прямо сейчас."""

HELP_TEXT = """Что я умею:

— Жалобы в УК, Роспотребнадзор, прокуратуру
— Претензии продавцам и сервисам
— Заявления работодателю
— Обращения в госорганы
— Деловые письма и объяснительные

Просто напиши текст своими словами — я переведу.
Если хочешь конкретный тип документа, укажи в начале:
_«жалоба: [твой текст]»_"""

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, parse_mode="Markdown")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT, parse_mode="Markdown")

@dp.message(F.text)
async def handle_text(message: Message):
    user_text = message.text.strip()
    if len(user_text) < 5:
        await message.answer("Напиши текст подлиннее — мне нужно что-то переводить.")
        return
    if len(user_text) > 3000:
        await message.answer("Текст слишком длинный. Пожалуйста, сократи до 3000 символов.")
        return

    thinking_msg = await message.answer("Перевожу...")

    try:
        response = await asyncio.to_thread(
            model.generate_content, user_text
        )
        result = response.text.strip()
        await thinking_msg.delete()
        await message.answer(result)
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        await thinking_msg.delete()
        await message.answer("Что-то пошло не так. Попробуй ещё раз через минуту.")

async def main():
    logger.info("Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
