import os
import logging

from environs import Env
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.types import ContentType
from aiogram import F

from config import UPLOAD_FOLDER, RESULT_FOLDER
from models.RealESRGAN import  process_input
env = Env()
env.read_env()
#env.read_env(os.path.join('..', '.env'))

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Халоу, это бот-супер-резолютер. Пришли картинку и я попробую в 2 раза увеличить ее разрешение')

@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer('Пришли картинку и я попробую в 2 раза увеличить ее разрешение')

@dp.message(F.content_type == ContentType.PHOTO)
async def process_photo(message: Message):
    await message.answer('начинаю супер резолютить')
    #https: // qna.habr.com / q / 1239494
    #https://qna.habr.com/q/1317156
    #file_name = f"photos/{message.photo[-1].file_id}.jpg"
    #file_name = f"{UPLOAD_FOLDER}/{message.chat_id}_{message.photo[-1].file_id}.jpg"
    f_path = f"{UPLOAD_FOLDER}/{message.message_id}_{message.photo[-1].file_id}.jpg"
    print('img_file_name', f_path)
    await bot.download(file=message.photo[-1].file_id, destination=f_path)

    #await photo.download()
    res_f_name = await process_input(f_path)
    logging.info(f'{res_f_name} сохранен')
    await message.answer(res_f_name)
    #await message.reply_photo(message.photo[-1].file_id) # reply_to_message_id

@dp.message()
async def process_other_messages(message: Message):
    await message.reply('Жду фото в низком разрешении')


if __name__ == '__main__':
    dp.run_polling(bot)
