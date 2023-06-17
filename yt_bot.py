from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from pytube import YouTube
import os

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

format_buttons = [
    KeyboardButton('Mp3'),
    KeyboardButton('Mp4')
]

format_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*format_buttons)

class FormatState(StatesGroup):
    url = State()
    format_url = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}!\n"
                         "Я помогу тебе скачать видео или аудио с YouTube. Просто отправь ссылку на YouTube.")

@dp.message_handler()
async def get_youtube_url(message: types.Message, state: FSMContext):
    if 'https://youtu.be/' in message.text:
        await message.reply("В каком формате вы хотите получить результат?", reply_markup=format_keyboard)
        await FormatState.url.set()
        await state.update_data(url=message.text)
    else:
        await message.reply("Неправильный формат ссылки")

@dp.message_handler(state=FormatState.url)
async def download(message: types.Message, state: FSMContext):
    data = await state.get_data()
    url = data.get('url')
    yt = YouTube(url, use_oauth=True)

    if message.text == 'Mp3':
        await message.answer("Скачиваем аудио, ожидайте...")
        yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')
        await message.answer("Скачалось, отправляю...")

        with open(f'audio/{yt.title}.mp3', 'rb') as audio:
            await bot.send_audio(message.chat.id, audio)

        os.remove(f'audio/{yt.title}.mp3')

    elif message.text == 'Mp4':
        await message.answer("Скачиваем видео, ожидайте...")
        yt.streams.get_highest_resolution().download('video', f'{yt.title}.mp4')
        await message.answer("Скачалось, отправляю...")

        with open(f'video/{yt.title}.mp4', 'rb') as video:
            await bot.send_video(message.chat.id, video)

        os.remove(f'video/{yt.title}.mp4')

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
