from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.ru import LEXICON
from services.file_handling import book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    bookmarks_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        bookmarks_kb.row(InlineKeyboardButton(
                            text=f'{button} - {book[button][:100]}',
                            callback_data=str(button)))
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    bookmarks_kb.row(InlineKeyboardButton(
        text=LEXICON['edit_bookmarks_button'],
        callback_data='edit_bookmarks'),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        ),
        width=2
    )
    return bookmarks_kb.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    bookmarks_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        bookmarks_kb.row(InlineKeyboardButton(
                    text=f'{LEXICON["del"]} {button} - {book[button][:100]}',
                    callback_data=f'{button}del'))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    bookmarks_kb.row(InlineKeyboardButton(
        text=LEXICON['cancel'],
        callback_data='cancel'),
        width=2
    )
    return bookmarks_kb.as_markup()
