from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode

from settings import bot_config

bot = Bot(token=bot_config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)