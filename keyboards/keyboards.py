from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.ru import LEXICON_RU


button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

yes_no_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_yes, button_no]],
    one_time_keyboard=True,
    resize_keyboard=True
)

button_rock: KeyboardButton = KeyboardButton(text=LEXICON_RU['rock'])
button_scissors: KeyboardButton = KeyboardButton(text=LEXICON_RU['scissors'])
button_paper: KeyboardButton = KeyboardButton(text=LEXICON_RU['paper'])

game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_rock, button_scissors, button_paper]],
    resize_keyboard=True
)

