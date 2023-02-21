import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, Message
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import Config, load_config

logger = logging


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

    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Релакс музыка для души',
        url='https://www.youtube.com/watch?v=jfKfPfyJRdk')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Документация Telegram Bot API',
        url='https://core.telegram.org/bots/api')
    url_button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Группа "Телеграм-боты на AIOgram"',
        url='tg://resolve?domain=aiogram_stepik_course'
    )
    url_button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='Автор этого чуда',
        url='tg://user?id=624627294'
    )
    url_button_5: InlineKeyboardButton = InlineKeyboardButton(
        text='Канал "Стать специалистом по машинному обучению"',
        url='https://t.me/toBeAnMLspecialist'
    )

    kp_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kp_builder.add(*[url_button_1, url_button_2, url_button_3, url_button_4, url_button_5])
    kp_builder.adjust(2, 1, repeat=True)

    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
            text='Это инлайн-кнопки с параметром "url"',
            reply_markup=kp_builder.as_markup(resize_keyboard=True),
            resize_keyboard=True
        )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
