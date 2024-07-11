import os
import asyncio
import requests
from environs import Env
from config import RESULT_FOLDER, API_URL


env = Env()
env.read_env(os.path.join('..', '.env'))

BOT_TOKEN = env('BOT_TOKEN')

