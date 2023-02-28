import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message, InlineKeyboardMarkup, InputMediaAudio, \
    InputMediaDocument, InputMediaPhoto, InputMediaVideo
from aiogram.filters import Command, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_data.config import Config, load_config

logger = logging.getLogger(__name__)

LEXICON: dict[str, str] = {
    'audio': '🎶 Аудио',
    'text': '📃 Текст',
    'photo': '🖼 Фото',
    'video': '🎬 Видео',
    'document': '📑 Документ',
    'voice': '📢 Голосовое сообщение',
    'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
    'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
    'photo_id1': 'AgACAgIAAxkBAAICRmP8mIiTtfJzxvBF5YWUq69TBTA1AALuxDEbG_boS0_UTR0p3oMxAQADAgADcwADLgQ',
    'photo_id2': 'AgACAgIAAxkBAAICSGP8mI-W-_gS0lY_fylIRaM5yKl-AALwxDEbG_boSySYSVs1dii5AQADAgADcwADLgQ',
    'voice_id1': 'AwACAgIAAxkBAAICTmP8mSSwgQ12PUczvhYx3TWeW1OKAAKMJAACG_boSwYk6LvXojTDLgQ',
    'voice_id2': 'AwACAgIAAxkBAAICUGP8mSlTA4lavD1ZwKZtMF_gIEr4AAKNJAACG_boS2GcC8VH8GXWLgQ',
    'audio_id1': 'CQACAgIAAxkBAAICWmP9qBoMYpIe1xNcZHt8FUY2JeM5AAKjIgACG_bwSySO_xdd7KmyLgQ',
    'audio_id2': 'CQACAgIAAxkBAAICW2P9qBpqzls34IRFfaTJDTaeMWoVAAKkIgACG_bwS-i35fsnKDnOLgQ',
    'document_id1': 'BQACAgIAAxkBAAICSmP8mNtL1E-hl9fTNXb-dNUAAXjB-QAChiQAAhv26EtWztZpFcy6DC4E',
    'document_id2': 'BQACAgIAAxkBAAICTGP8mOLsX6AF27eAQ5FNMNdbZOPRAAKHJAACG_boS0P1InypanEJLgQ',
    'video_id1': 'BAACAgIAAxkBAAICVmP8mf2mIj1IRWhwAY6HK-q78sd9AAKVJAACG_boSyy4JAvEQoD6LgQ',
    'video_id2': 'BAACAgIAAxkBAAICWGP8mhe2rQEnVGwAASpTlXm2c8qsQwACliQAAhv26EuouZeF-Blsky4E',
}


def add_markup() -> InlineKeyboardMarkup:
    markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text=LEXICON['audio'], callback_data='audio'))
    markup.add(InlineKeyboardButton(text=LEXICON['video'], callback_data='video'))
    markup.add(InlineKeyboardButton(text=LEXICON['photo'], callback_data='photo'))
    markup.add(InlineKeyboardButton(text=LEXICON['voice'], callback_data='voice'))
    markup.add(InlineKeyboardButton(text=LEXICON['document'], callback_data='document'))
    return markup.as_markup()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config('config_data/.env')

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Этот хэндлер будет срабатывать на команды "/start"
    async def process_start_command(message: Message):
        await message.answer_audio(
            audio=LEXICON['audio_id1'],
            caption='Это 1 аудио',
            reply_markup=add_markup()
        )

    # Этот хэндлер будет срабатывать на нажатие кнопки "audio!"
    async def change_on_audio(callback: CallbackQuery):
        await callback.message.edit_media(
            media=InputMediaAudio(
                media=LEXICON['audio_id2'],
                caption='Это 2 аудио'
            ),
            reply_markup=add_markup()
        )

    # Этот хэндлер будет срабатывать на нажатие кнопки "video!"
    async def change_on_video(callback: CallbackQuery):
        await callback.message.edit_media(
            media=InputMediaVideo(
                media=LEXICON['video_id1'],
                caption='Это 1 видео'
            ),
            reply_markup=add_markup()
        )

    # Этот хэндлер будет срабатывать на нажатие кнопки "photo!"
    async def change_on_photo(callback: CallbackQuery):
        await callback.message.edit_media(
            # chat_id=callback.message.chat.id, убираем
            # message_id=callback.message.message_id, убираем
            media=InputMediaPhoto(
                media=LEXICON['photo_id1'],
                caption='Это 1 photo'
            ),
            reply_markup=add_markup()
        )

    # Этот хэндлер будет срабатывать на нажатие кнопки "voice!"
    async def change_on_voice(callback: CallbackQuery):
        await callback.message.edit_media(
            media=InputMediaAudio(
                media=LEXICON['audio_id1'],
                caption='Это 1 аудио'
            ),
            reply_markup=add_markup()
        )

    # Этот хэндлер будет срабатывать на нажатие кнопки "doc!"
    async def change_on_doc(callback: CallbackQuery):
        await callback.message.edit_media(
            media=InputMediaDocument(
                media=LEXICON['document_id1'],
                caption='Это 1 doc'
            ),
            reply_markup=add_markup()
        )

    # Этот хэндлер будет срабатывать на любые сообщения, кроме команд
    async def send_echo(message: Message):
        await message.answer(
            text='Я даже представить себе не могу, '
                 'что ты имеешь в виду'
        )

    dp.message.register(process_start_command, Command(commands=['start']))
    dp.callback_query.register(change_on_audio, Text(text='audio'))
    dp.callback_query.register(change_on_video, Text(text='video'))
    dp.callback_query.register(change_on_photo, Text(text='photo'))
    dp.callback_query.register(change_on_doc, Text(text='document'))
    dp.callback_query.register(change_on_voice, Text(text='voice'))
    dp.message.register(send_echo)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
