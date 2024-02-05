import logging
import sys

from aiogram.filters import CommandStart
from aiogram.types import Message

from database import orm
import handlers
from keyboards.default.menu import *
from loader import bot, dp


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
