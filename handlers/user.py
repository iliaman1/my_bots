from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command

from lexicon.ru import LEXICON_RU
from keyboards.keyboards import yes_no_kb, game_kb
from services.services import get_bot_choise, get_winner


async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


async def process_game_button(message: Message):
    bot_choise = get_bot_choise()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} - {LEXICON_RU[bot_choise]}')
    winner = get_winner(message.text, bot_choise)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)


def register_user_handlers(dp: Dispatcher):
    dp.message.register(process_start_command, Command(commands=["start"]))
    dp.message.register(process_help_command, Command(commands=['help']))
    dp.message.register(process_yes_answer, Text(text=LEXICON_RU['yes_button']))
    dp.message.register(process_no_answer, Text(text=LEXICON_RU['no_button']))
    dp.message.register(process_game_button, Text(text=[
        LEXICON_RU['rock'],
        LEXICON_RU['paper'],
        LEXICON_RU['scissors']
    ]))
