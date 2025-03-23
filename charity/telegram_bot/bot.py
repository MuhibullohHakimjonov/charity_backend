from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiohttp
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://127.0.0.1:8000/telegram/questions/"
RESPONSE_API_URL = "http://127.0.0.1:8000/telegram/responses/"
PHONE_SAVE_API_URL = "http://127.0.0.1:8000/telegram/save_phone/"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()


class QuizState(StatesGroup):
    waiting_for_phone = State()
    question_index = State()
    questions = State()


async def fetch_questions():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            return await response.json()


@router.message(CommandStart())
async def start_quiz(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Share Phone Number", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer("Please share your phone number to proceed:", reply_markup=keyboard)
    await state.set_state(QuizState.waiting_for_phone)


@router.message(QuizState.waiting_for_phone)
async def save_phone_number(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer("Please use the button to share your phone number.")
        return

    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username

    payload = {
        "user_id": user_id,
        "username": username,
        "phone_number": phone_number
    }

    async with aiohttp.ClientSession() as session:
        await session.post(PHONE_SAVE_API_URL, json=payload)

    await message.answer("Phone number saved! Let's start the quiz.")

    questions = await fetch_questions()
    if not questions:
        await message.answer("No questions available.")
        return

    await state.update_data(questions=questions, current_index=0)
    await state.set_state(QuizState.question_index)
    await send_next_question(message, state)


async def send_next_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions", [])
    index = data.get("current_index", 0)

    if index < len(questions):
        await message.answer(questions[index]["text"])
        await state.update_data(current_index=index + 1, last_question_id=questions[index]["id"])
    else:
        await message.answer("You've completed all questions!")
        await state.clear()


@router.message(QuizState.question_index)
async def handle_response(message: types.Message, state: FSMContext):
    data = await state.get_data()
    last_question_id = data.get("last_question_id")

    if last_question_id:
        payload = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "question": last_question_id,
            "response": message.text,
        }

        async with aiohttp.ClientSession() as session:
            await session.post(RESPONSE_API_URL, json=payload)

    await send_next_question(message, state)


dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
