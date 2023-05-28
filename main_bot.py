import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from keyboards.main_keyboards import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config: Config = load_config('config_data/.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')