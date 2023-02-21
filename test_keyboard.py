import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, KeyboardButtonPollType)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config_data.config import load_config

config = load_config('config_data/.env')

bot_token = config.tg_bot.token

bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()

# # Создаем объекты кнопок
# button_1: KeyboardButton = KeyboardButton(text='Собак 🦮')
# button_2: KeyboardButton = KeyboardButton(text='Огурцов 🥒')
#
# # Создаем объект клавиатуры, добавляя в него кнопки
# keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
#     keyboard=[[button_1, button_2]],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )


kp_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
buttons_1: list[KeyboardButton] = [
    KeyboardButton(text='Собак 🦮'),
    KeyboardButton(text='Огурцов 🥒'),
    KeyboardButton(text='Отправить телефон', request_contact=True),
    KeyboardButton(text='Отправить геолокацию', request_location=True),
    KeyboardButton(text='Создать викторину/опрос', request_poll=KeyboardButtonPollType()),
    KeyboardButton(text='Собак 🦮'),
    KeyboardButton(text='Огурцов 🥒')
]
buttons_2: list[KeyboardButton] = [KeyboardButton(text=f'Кнопка {i + 6}') for i in range(4)]
# kp_builder.row(*buttons_1, width=4)
# kp_builder.row(*buttons_2, width=3)
# # ля как через метод add
# kp_builder.add(*buttons_2)
# # ля как через add и adjust
kp_builder.add(*buttons_1)
kp_builder.adjust(2, 1, repeat=True)


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Чего кошки боятся больше? Заодно зацени клаву)',
                         reply_markup=kp_builder.as_markup(resize_keyboard=True))


# Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
@dp.message(Text(text='Собак 🦮'))
async def process_dog_answer(message: Message):
    cat_response = requests.get('https://aws.random.cat/meow')

    if cat_response.status_code == 200:
        cat_link = cat_response.json()['file']
        await bot.send_photo(chat_id=message.chat.id, photo=cat_link)
    else:
        await bot.send_message(chat_id=message.chat.id, text='тут мог быть котик')
    await message.answer(text='Да, несомненно, кошки боятся собак. '
                              'Но вы видели как они боятся огурцов?')


# Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
@dp.message(Text(text='Огурцов 🥒'))
async def process_cucumber_answer(message: Message):
    cat_response = requests.get('https://aws.random.cat/meow')

    if cat_response.status_code == 200:
        cat_link = cat_response.json()['file']
        await bot.send_photo(chat_id=message.chat.id, photo=cat_link)
    else:
        await bot.send_message(chat_id=message.chat.id, text='тут мог быть котик')
    await message.answer(text='Да, иногда кажется, что огурцов '
                              'кошки боятся больше')


if __name__ == '__main__':
    dp.run_polling(bot)
