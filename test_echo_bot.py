from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from config_data.config import load_config
from pprint import pprint

config = load_config('config_data/.env')

bot_token = config.tg_bot.token

bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Не павук!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
async def send_echo(message: Message):
    await bot.send_message(message.chat.id, message.text)


# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    print(message.photo[0].file_id)
    await message.reply_photo(message.photo[0].file_id)


# Этот хэндлер будет срабатывать на отправку боту Аудио
async def send_audio_echo(message: Message):
    print(message.audio.file_id)
    await message.reply_audio(message.audio.file_id)


# Этот хэндлер будет срабатывать на отправку боту Видео
async def send_video_echo(message: Message):
    print(message.video.file_id)
    await message.reply_video(message.video.file_id)


# Этот хэндлер будет срабатывать на отправку боту Стикера
async def send_sticker_echo(message: Message):
    await message.reply_sticker(message.sticker.file_id)


# Этот хэндлер будет срабатывать на отправку боту Документа
async def send_document_echo(message: Message):
    print(message.document.file_id)
    await message.reply_document(message.document.file_id)


# Этот хэндлер будет срабатывать на отправку боту Voice message
async def send_voice_echo(message: Message):
    print(message.voice.file_id)
    await message.reply_voice(message.voice.file_id)


# Этот хэндлер будет срабатывать на отправку боту анимации
async def send_animation_echo(message: Message):
    print(message.animation.file_id)
    await message.reply_animation(message.animation.file_id)


dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(send_photo_echo, F.photo)
dp.message.register(send_audio_echo, F.audio)
dp.message.register(send_video_echo, F.video)
dp.message.register(send_sticker_echo, F.sticker)
dp.message.register(send_document_echo, F.document)
dp.message.register(send_voice_echo, F.voice)
dp.message.register(send_animation_echo, F.animation)
dp.message.register(send_echo)


if __name__ == '__main__':
    dp.run_polling(bot)


# Через send_copy
# from aiogram import Bot, Dispatcher
# from aiogram.filters import Command
# from aiogram.types import Message
#
# # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# # полученный у @BotFather
# API_TOKEN: str = 'BOT TOKEN HERE'
#
# # Создаем объекты бота и диспетчера
# bot: Bot = Bot(token=API_TOKEN)
# dp: Dispatcher = Dispatcher()
#
#
# # Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(Command(commands=["start"]))
# async def process_start_command(message: Message):
#     await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')
#
#
# # Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=["help"]))
# async def process_help_command(message: Message):
#     await message.answer('Напиши мне что-нибудь и в ответ '
#                          'я пришлю тебе твое сообщение')
#
#
# # Этот хэндлер будет срабатывать на любые ваши сообщения,
# # кроме команд "/start" и "/help"
# @dp.message()
# async def send_echo(message: Message):
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.reply(text='Данный тип апдейтов не поддерживается '
#                                  'методом send_copy')
#
#
# if __name__ == '__main__':
#     dp.run_polling(bot)