import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers.other import register_echo_handler
from handlers.user import register_user_handlers
from keyboards.set_menu import set_main_menu


logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher) -> None:
    register_user_handlers(dp)
    register_echo_handler(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config('config_data/.env')

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
