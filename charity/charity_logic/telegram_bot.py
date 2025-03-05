import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = ""
DJANGO_API_URL = "http://127.0.0.1:8000/register-user/"
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def send_user_data(user_data):
    """Send user data to Django API"""
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        async with session.post(DJANGO_API_URL, json=user_data, headers=headers) as response:
            return await response.text()


@dp.message(Command("start"))
async def start_command(message: Message):
    """Handle /start and send user info to Django"""
    user_data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or "No Username",
    }

    response = await send_user_data(user_data)
    print("Django Response:", response)

    await message.answer("👋 Welcome! You have been registered.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
