import asyncio
import logging
import random

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.filters import Command, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import Config, load_config
from lexicon.ru import JOKES

logger = logging.getLogger(__name__)


def random_joke() -> int:
    return random.randint(1, len(JOKES))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config('config_data/.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Этот хэндлер будет срабатывать на команды "/start" и "/joke"
    async def process_start_command(message: Message):
        markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
        markup.add(InlineKeyboardButton(text='Хочу еще!', callback_data='more'))
        await message.answer(
            text=JOKES[random_joke()],
            reply_markup=markup.as_markup()
        )

    # Этот хэндлер будет срабатывать на нажатие кнопки "Хочу еще!"
    async def process_more_press(callback: CallbackQuery):
        markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
        markup.add(InlineKeyboardButton(text='Хочу еще!', callback_data='more'))
        # await callback.answer() отвечаем на колбек
        # await callback.message.answer(text=text, reply_markup=klava) отправляем новое сообщение
        # await callback.message.delete() удаляем сообщение
        # Редактируем в чате сообщение с шуткой
        text = JOKES[random_joke()]
        while text == callback.message.text:
            text = JOKES[random_joke()]
        await callback.message.edit_text(
            text=text,
            reply_markup=markup.as_markup()
        )

    # Этот хэндлер будет срабатывать на любые сообщения, кроме команд
    async def send_echo(message: Message):
        await message.answer(
            text='Я даже представить себе не могу, '
                 'что ты имеешь в виду :(\n\n'
                 'Чтобы получить какую-нибудь шутку - '
                 'отправь команду /joke')

    dp.message.register(process_start_command, Command(commands=['start', 'joke']))
    dp.message.register(send_echo)
    dp.callback_query.register(process_more_press, Text(text='more'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
