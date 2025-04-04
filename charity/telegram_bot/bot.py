import os
import aiohttp
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

API_BASE_URL = "http://127.0.0.1:8000/telegram"
API_URL_QUESTIONS = f"{API_BASE_URL}/questions/"
API_URL_RESPONSES = f"{API_BASE_URL}/responses/"
API_URL_SAVE_PHONE = f"{API_BASE_URL}/save_phone/"
API_URL_AUDIO = f"{API_BASE_URL}/get_audio/"
API_URL_CHECK_USER = f"{API_BASE_URL}/check_user/"

logging.basicConfig(level=logging.INFO)


class QuizState(StatesGroup):
    waiting_for_phone = State()
    answering_questions = State()


async def fetch_json(url):
    """Helper function to fetch JSON data from an API endpoint."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None


async def check_user_status(user_id: int):
    """Check if the user is registered and has completed the quiz."""
    url = f"{API_URL_CHECK_USER}{user_id}/"
    data = await fetch_json(url)
    return data.get("status") if data else "not_registered"


@router.message(CommandStart())
async def start_quiz(message: types.Message, state: FSMContext):
    """Start quiz process by checking user status and registering if needed."""
    user_id = message.from_user.id
    status = await check_user_status(user_id)

    if status == "completed":
        await message.answer("🎉 You have already completed the quiz!")
        return
    elif status == "registered":
        await message.answer("✅ You are already registered! Starting the quiz now...")
        await send_audio_message(message)
        await start_questions(message, state)
        return

    # Ask for phone number if not registered
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="📱 Share Phone Number", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer("Please share your phone number to proceed:", reply_markup=keyboard)
    await state.set_state(QuizState.waiting_for_phone)


@router.message(QuizState.waiting_for_phone)
async def save_phone_number(message: types.Message, state: FSMContext):
    """Save user's phone number and proceed to the quiz."""
    if not message.contact:
        await message.answer("⚠️ Please use the button to share your phone number.")
        return

    payload = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or "Unknown",
        "phone_number": message.contact.phone_number,
    }

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(API_URL_SAVE_PHONE, json=payload)
            if response.status != 201:
                await message.answer("❌ Failed to save your phone number. Please try again.")
                return
    except Exception as e:
        logging.error(f"Error saving phone number: {e}")
        await message.answer("❌ Error saving your phone number. Please try again.")
        return

    await message.answer("✅ Phone number saved! Now, listen to this audio before we start the quiz.")
    await send_audio_message(message)
    await start_questions(message, state)


async def send_audio_message(message: types.Message):
    """Fetch and send the admin-uploaded MP3 audio as a voice message."""
    data = await fetch_json(API_URL_AUDIO)
    audio_url = data.get("audio_url") if data else None

    if not audio_url:
        await message.answer("⚠️ No audio file available.")
        return

    # Ensure audio URL is absolute
    if audio_url.startswith("/"):
        audio_url = f"http://127.0.0.1:8000{audio_url}"  # Adjust base URL if different

    async with aiohttp.ClientSession() as session:
        async with session.get(audio_url) as audio_response:
            if audio_response.status != 200:
                await message.answer("⚠️ Error: Could not fetch the audio file.")
                return

            file_name = "audio.ogg"
            with open(file_name, "wb") as f:
                f.write(await audio_response.read())

            with open(file_name, "rb") as audio:
                await bot.send_voice(chat_id=message.chat.id, voice=BufferedInputFile(audio.read(), filename=file_name))
            os.remove(file_name)


async def fetch_questions():
    """Fetch all quiz questions."""
    return await fetch_json(API_URL_QUESTIONS) or []


async def start_questions(message: types.Message, state: FSMContext):
    """Start the quiz by fetching and sending the first question."""
    questions = await fetch_questions()
    if not questions:
        await message.answer("❌ No questions available.")
        return

    await state.update_data(questions=questions, current_index=0, answers=[])
    await state.set_state(QuizState.answering_questions)
    await send_next_question(message, state)


async def send_next_question(message: types.Message, state: FSMContext):
    """Send the next question or finish the quiz."""
    data = await state.get_data()
    questions = data["questions"]
    index = data["current_index"]

    if index >= len(questions):
        await save_all_responses(state)
        await message.answer("🎉 Quiz completed! Thank you for your responses.")
        await state.clear()
        return

    question = questions[index]
    await message.answer(question["text"])

    await state.update_data(current_index=index + 1, last_question_id=question["id"])


async def save_all_responses(user_responses):
    """Send all responses to the API when the quiz is fully completed."""
    if not user_responses:
        return

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(API_URL_RESPONSES, json={"responses": user_responses})
            if response.status != 201:
                logging.error(f"❌ Failed to save responses: {await response.text()}")
    except Exception as e:
        logging.error(f"❌ Error saving responses: {e}")


@router.message(QuizState.answering_questions)
async def handle_response(message: types.Message, state: FSMContext):
    """Temporarily store responses and submit only when the quiz is completed."""
    data = await state.get_data()
    questions = data.get("questions", [])
    index = data.get("current_index", 0)
    user_responses = data.get("user_responses", [])

    if index > 0:
        last_question = questions[index - 1]
        user_responses.append({
            "user_id": message.from_user.id,
            "username": message.from_user.username or "Unknown",
            "question": last_question["id"],
            "response": message.text,
        })
    if index >= len(questions):
        await save_all_responses(user_responses)
        await message.answer("🎉 Quiz completed! Your responses have been saved.")
        await state.clear()
        return

    await state.update_data(user_responses=user_responses, current_index=index)
    await send_next_question(message, state)


dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
