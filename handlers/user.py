from copy import deepcopy

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from db_interaction.database import user_dict_template, users_db
from keyboards.bookmarks_kb import (
    create_bookmarks_keyboard,
    create_edit_keyboard
)
from keyboards.pagination_kb import create_pagination_keyboard

from lexicon.ru import LEXICON
from lexicon.ru import LEXICON_RU
from services.file_handling import book
from keyboards.keyboards import yes_no_kb, game_kb
from services.services import get_bot_choise, get_winner


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        ).as_markup(resize_keyboard=True)
    )


# Этот хэндлер будет срабатывать на команду "continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        ).as_markup(resize_keyboard=True)
    )


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]
            ).as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            ).as_markup(resize_keyboard=True)
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            ).as_markup(resize_keyboard=True)
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        ).as_markup(resize_keyboard=True)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]["bookmarks"]
        ).as_markup(resize_keyboard=True)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(*users_db[callback.from_user.id]["bookmarks"]).as_markup(
                resize_keyboard=True)
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()


# Функция для регистрации хэндлеров пользователя в диспетчере
def register_user_handlers(dp: Dispatcher):
    dp.message.register(process_start_command, commands=['start'])
    dp.message.register(process_help_command, commands=['help'])
    dp.message.register(
        process_beginning_command,
        commands=['beginning']
    )
    dp.message.register(
        process_continue_command,
        commands=['continue']
    )
    dp.message.register(
        process_bookmarks_command,
        commands=['bookmarks']
    )

    dp.callback_query.register(process_forward_press, text="forward")
    dp.callback_query.register(process_backward_press, text="backward")
    dp.callback_query.register(
        process_page_press,
        lambda x: '/' in x.data and x.data.replace('/', '').isdigit()
    )
    dp.callback_query.register(
        process_bookmark_press,
        lambda x: x.data.isdigit()
    )
    dp.callback_query.register(process_edit_press, text="edit_bookmarks")
    dp.callback_query.register(process_cancel_press, text="cancel")
    dp.callback_query.register(
        process_del_bookmark_press,
        lambda x: 'del' in x.data and x.data[:-3].isdigit()
    )


async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


async def process_game_button(message: Message):
    bot_choise = get_bot_choise()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} - {LEXICON_RU[bot_choise]}')
    winner = get_winner(message.text, bot_choise)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)

# def register_user_handlers(dp: Dispatcher):
#     dp.message.register(process_start_command, Command(commands=["start"]))
#     dp.message.register(process_help_command, Command(commands=['help']))
#     dp.message.register(process_yes_answer, Text(text=LEXICON_RU['yes_button']))
#     dp.message.register(process_no_answer, Text(text=LEXICON_RU['no_button']))
#     dp.message.register(process_game_button, Text(text=[
#         LEXICON_RU['rock'],
#         LEXICON_RU['paper'],
#         LEXICON_RU['scissors']
#     ]))
