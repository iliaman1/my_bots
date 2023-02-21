from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command, BaseFilter
from config_data.config import load_config

config = load_config('config_data/.env')

bot_token = config.tg_bot.token

bot: Bot = Bot(bot_token)
dp: Dispatcher = Dispatcher()

from typing import Any


# ...

# Какой-то фильтр
class MyFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, Any]:
        # Какой-то код
        # ...
        # Какой-то код
        return {'key_1': 'value_1',
                'key_2': 'value_2',
                'key_3': 'value_3'}


# ...

# Какой-то хэндлер
@dp.message(MyFilter())
async def some_handler(message: Message,
                       key_1: str,
                       key_2: str,
                       key_3: str):
    await  message.answer(f'Получилось передать из фильтра {key_1}{key_2}{key_3}')


if __name__ == '__main__':
    dp.run_polling(bot)
