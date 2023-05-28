from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, Text
from lexicon.main_ru import ANSWER_ON_COMMANDS_RU


async def process_start_command(message: Message):
    await message.answer(ANSWER_ON_COMMANDS_RU[message.text])
