from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.ru import LEXICON


# Функция, генерирующая клавиатуру для страницы книги
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardBuilder:
    # Создаем объект клавиатуры
    pagination_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками
    pagination_kb.row(*[InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                                             callback_data=button) for button in buttons])
    return pagination_kb
