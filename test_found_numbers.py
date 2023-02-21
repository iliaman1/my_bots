from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command, BaseFilter
from config_data.config import load_config

config = load_config('config_data/.env')

bot_token = config.tg_bot.token

bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()


class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        if numbers:
            return {'numbers': numbers}

        return False


@dp.message(Text(startswith='найди числа', ignore_case=True), NumbersInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(
        text=f'Нашел: {str(", ".join(str(num) for num in numbers))}'
    )


@dp.message(Text(startswith='найди числа', ignore_case=True))
async def process_if_not_numbers(message: Message):
    await message.answer(
        text='Робот число не найдень :_-('
    )


if __name__ == '__main__':
    dp.run_polling(bot)
