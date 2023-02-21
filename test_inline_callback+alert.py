import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart, Text
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
        text='button 1',
        callback_data='button 1 pressed userom')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='button 2',
        callback_data='button 2 pressed userom')

    kp_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kp_builder.add(*[url_button_1, url_button_2])
    kp_builder.adjust(1, repeat=True)

    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
            text='Это инлайн-кнопки с параметром "callback"',
            reply_markup=kp_builder.as_markup(resize_keyboard=True),
            resize_keyboard=True
        )

    @dp.callback_query(Text(text=['button 1 pressed userom']))
    async def process_button1_press(callback: CallbackQuery):
        if callback.message.text != 'была нажата кнопка 1':
            await callback.message.edit_text(
                text='была нажата кнопка 1',
                reply_markup=callback.message.reply_markup
            )
        await callback.answer(text='Нажата кнопка 1', show_alert=True)

    @dp.callback_query(Text(text=['button 2 pressed userom']))
    async def process_button1_press(callback: CallbackQuery):
        if callback.message.text != 'была нажата кнопка 2':
            await callback.message.edit_text(
                text='была нажата кнопка 2',
                reply_markup=callback.message.reply_markup
            )
        await callback.answer(text='Нажата кнопка 2')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
