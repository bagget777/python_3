from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from pytube import YouTube
import sqlite3, time, logging, os

if not os.path.exists('video'):
    os.makedirs('video')

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# Create the "video" folder if it doesn't exist
if not os.path.exists('video'):
    os.makedirs('video')

database = sqlite3.connect('youtube.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INT,
    chat_id INT,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    created VARCHAR(100)
);
""")
cursor.connection.commit()

# Rest of the code...
