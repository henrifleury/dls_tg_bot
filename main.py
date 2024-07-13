# import os
import logging
import asyncio

from environs import Env
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import ContentType
from aiogram import F
from time import time

from config import UPLOAD_FOLDER, LOG_LEVEL
from resolutor import main as resolutor
from sender import main as sender
from threading import Thread
from aiofiles.os import listdir


logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

env = Env()
env.read_env()


BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет, это бот-улучшатель изображений. Пришли картинку и я попробую/'
        ' в 2 раза увеличить ее разрешение')


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer('Пришли картинку и я попробую в 2 раза увеличить ее/'
                         ' разрешение')


@dp.message(F.content_type == ContentType.PHOTO)
async def process_photo(message: Message):
    f_path = f"{UPLOAD_FOLDER}/{time()}_{message.message_id}"
    f_path += f"_{message.chat.id}_{message.photo[-1].file_id}.jpg"
    await bot.download(file=message.photo[-1].file_id, destination=f_path)
    img_list = await listdir(UPLOAD_FOLDER)
    q_len = len(img_list)
    if q_len > 1:
        await message.answer(f'Ждите ответа, в очереди на увеличение'
                             f' разрешения {q_len} файла(ов)')

    logger.info(f'{f_path} получен')


@dp.message()
async def process_other_messages(message: Message):
    await message.reply('Жду картинку в низком разрешении')

if __name__ == '__main__':
    # TODO all threads safe termination
    Thread(target=asyncio.run, args=(sender(),)).start()
    Thread(target=asyncio.run, args=(resolutor(),)).start()
    dp.run_polling(bot)
