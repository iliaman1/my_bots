from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import BotCommand
from config_data.config import load_config

config = load_config('config_data/.env')

bot_token = config.tg_bot.token

bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help', description='справка'),
        BotCommand(command='/test1', description='справка1'),
        BotCommand(command='/test2', description='справка2'),
        BotCommand(command='/test3', description='справка3'),
    ]

    await bot.set_my_commands(main_menu_commands)


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
