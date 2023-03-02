import logging
import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import Config, load_config
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger(__name__)


async def set_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help', description='Справка'),
        BotCommand(command='/start', description='Получить стартовое сообщение'),
        BotCommand(command='/fillform', description='Начать заполнение анкеты'),
        BotCommand(command='/showdata', description='Посмотреть данные вашей анкеты'),
        BotCommand(command='/cancel', description='Прервать заполнение анкеты'),
    ]

    await bot.set_my_commands(main_menu_commands)


def fill_gender_keyboard() -> InlineKeyboardMarkup:
    mk_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    male_button = InlineKeyboardButton(
        text='Мужской ♂',
        callback_data='male'
    )
    female_button = InlineKeyboardButton(
        text='Женский ♀',
        callback_data='female'
    )
    undefined_button = InlineKeyboardButton(
        text='🤷 Пока не ясно',
        callback_data='undefined_gender'
    )
    return mk_builder.row(*[male_button, female_button, undefined_button], width=2).as_markup(resize_keyboard=True)


def fill_education_keyboard() -> InlineKeyboardMarkup:
    mk_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    secondary_button = InlineKeyboardButton(
        text='Среднее',
        callback_data='secondary'
    )
    higher_button = InlineKeyboardButton(
        text='Высшее',
        callback_data='higher'
    )
    no_edu_button = InlineKeyboardButton(
        text='🤷 Нету',
        callback_data='no_edu'
    )
    return mk_builder.row(*[secondary_button, higher_button, no_edu_button], width=2).as_markup(resize_keyboard=True)


def subscribe_news_accept() -> InlineKeyboardMarkup:
    mk_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    yes_news_button = InlineKeyboardButton(
        text='Да',
        callback_data='yes_news'
    )
    no_news_button = InlineKeyboardButton(
        text='Нет, спасибо',
        callback_data='no_news'
    )
    return mk_builder.row(*[yes_news_button, no_news_button]).as_markup(resize_keyboard=True)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config('config_data/.env')

    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    user_dict: dict[int, dict[str, str | int]] = {}

    class FSMFillForm(StatesGroup):
        fill_name = State()
        fill_age = State()
        fill_gender = State()
        upload_photo = State()
        fill_education = State()
        fill_wish_news = State()

    async def process_start_command(message: Message):
        await message.answer(
            text='Этот бот демонстрирует работу FSM\n\n'
                 'Чтобы перейти к заполнению анкеты - '
                 'отправьте команду /fillform'
        )

    async def process_fillform_command(message: Message, state: FSMContext):
        await message.answer(
            text='Пожалуйста введите выше имя',
        )
        await state.set_state(FSMFillForm.fill_name)

    async def warning_not_name(message: Message):
        await message.answer(
            text='То, что вы отправили не похоже на имя\n\n'
                 'Пожалуйста, введите ваше имя\n\n'
                 'Если вы хотите прервать заполнение анкеты - '
                 'отправьте команду /cancel'
        )

    async def process_name_sent(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer(text=f"Спасибо, {message.text}!\n\nА теперь введите ваш возраст")
        await state.set_state(FSMFillForm.fill_age)

    async def warning_not_age(message: Message):
        await message.answer(
            text='Возраст должен быть целым числом от 4 до 120\n\n'
                 'Попробуйте еще раз\n\nЕсли вы хотите прервать '
                 'заполнение анкеты - отправьте команду /cancel'
        )

    async def process_age_sent(message: Message, state: FSMContext):
        await state.update_data(age=int(message.text))
        current_data = await state.get_data()
        await message.answer(
            text=f"Спасибо, {current_data['name']}!\n\nУкажите ваш пол",
            reply_markup=fill_gender_keyboard()
        )
        await state.set_state(FSMFillForm.fill_gender)

    async def warning_not_gender(message: Message):
        await message.answer(
            text='Пожалуйста, пользуйтесь кнопками '
                 'при выборе пола\n\nЕсли вы хотите прервать '
                 'заполнение анкеты - отправьте команду /cancel'
        )

    async def process_gender_sent(callback: CallbackQuery, state: FSMContext):
        await state.update_data(gender=callback.data)
        await callback.message.delete()
        await callback.message.answer(
            text='Спасибо! А теперь загрузите, '
                 'пожалуйста, ваше фото'
        )
        await state.set_state(FSMFillForm.upload_photo)

    async def warning_not_photo(message: Message):
        await message.answer(
            text='Пожалуйста, на этом шаге отправьте '
                 'ваше фото\n\nЕсли вы хотите прервать '
                 'заполнение анкеты - отправьте команду /cancel'
        )

    async def process_photo_sent(message: Message, state: FSMContext):
        await state.update_data(photo_unique_id=message.photo[0].file_unique_id, photo_id=message.photo[0].file_id)
        await message.answer(
            text='Спасибо!\n\nУкажите ваше образование',
            reply_markup=fill_education_keyboard()
        )
        await state.set_state(FSMFillForm.fill_education)

    async def warning_not_education(message: Message):
        await message.answer(
            text='Пожалуйста, пользуйтесь кнопками '
                 'при выборе образования\n\nЕсли вы хотите '
                 'прервать заполнение анкеты - отправьте '
                 'команду /cancel'
        )

    async def process_education_press(callback: CallbackQuery, state: FSMContext):
        await state.update_data(education=callback.data)
        await callback.message.edit_text(
            text='Спасибо!\n\n'
                 'Остался последний шаг.\n'
                 'Хотели бы вы получать новости?',
            reply_markup=subscribe_news_accept()
        )
        await state.set_state(FSMFillForm.fill_wish_news)

    async def warning_not_wish_news(message: Message):
        await message.answer(
            text='Пожалуйста, воспользуйтесь кнопками!\n\n'
                 'Если вы хотите прервать заполнение анкеты - '
                 'отправьте команду /cancel'
        )

    async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
        await state.update_data(wish_news=True if callback.data == 'yes_news' else False)
        user_dict[callback.from_user.id] = await state.get_data()
        await state.clear()
        await callback.message.edit_text(
            text='Спасибо! Ваши данные сохранены!\n\n'
                 'Вы вышли из машины состояний'
        )
        await callback.message.answer(
            text='Чтобы посмотреть данные вашей '
                 'анкеты - отправьте команду /showdata'
        )

    async def process_showdata_command(message: Message):
        if message.from_user.id in user_dict:
            await message.answer_photo(
                photo=user_dict[message.from_user.id]['photo_id'],
                caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
                        f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
                        f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
                        f'Образование: {user_dict[message.from_user.id]["education"]}\n'
                        f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}'
            )
        else:
            await message.answer(
                text='Вы еще не заполняли анкету. '
                     'Чтобы приступить - отправьте '
                     'команду /fillform'
            )

    async def process_cancel_command(messasge: Message, state: FSMContext):
        await messasge.answer(
            text='Вы вышли из машины состояний\n\n'
                 'Чтобы снова перейти к заполнению анкеты - '
                 'отправьте команду /fillform'
        )
        await state.clear()

    async def send_echo(message: Message):
        await message.reply(
            text='Извините, моя твоя не понимать'
        )

    dp.message.register(process_start_command, Command(commands=['start']))
    dp.message.register(process_fillform_command, Command(commands=['fillform']))
    dp.message.register(process_cancel_command, Command(commands=['cancel']), StateFilter('*'))
    dp.message.register(process_showdata_command, Command(commands=['showdata']))

    dp.message.register(process_name_sent, FSMFillForm.fill_name, lambda x: x.text.isalpha())
    dp.message.register(warning_not_name, FSMFillForm.fill_name)
    dp.message.register(process_age_sent, FSMFillForm.fill_age, lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
    dp.message.register(warning_not_age, FSMFillForm.fill_age)

    dp.callback_query.register(process_gender_sent, FSMFillForm.fill_gender,
                               Text(text=['male', 'female', 'undefined_gender']))
    dp.message.register(warning_not_gender, FSMFillForm.fill_gender)
    dp.message.register(process_photo_sent, FSMFillForm.upload_photo, F.photo)
    dp.message.register(warning_not_photo, FSMFillForm.upload_photo)
    dp.callback_query.register(process_education_press, FSMFillForm.fill_education,
                               Text(text=['secondary', 'higher', 'no_edu']))
    dp.message.register(warning_not_education, FSMFillForm.fill_education)
    dp.callback_query.register(process_wish_news_press, FSMFillForm.fill_wish_news, Text(text=['yes_news', 'no_news']))
    dp.message.register(warning_not_wish_news, FSMFillForm.fill_wish_news)
    dp.message.register(send_echo)

    await set_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
