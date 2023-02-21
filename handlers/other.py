from aiogram import Dispatcher
from aiogram.types import Message

from lexicon.ru import LEXICON_RU


async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])


# Этот хэндлер будет реагировать на любые текстовые сообщения пользователя
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}')


def register_other_handlers(dp: Dispatcher):
    dp.message.register(send_answer)


# Функция для регистрации хэндлера
def register_echo_handler(dp: Dispatcher):
    dp.message.register(send_echo)
