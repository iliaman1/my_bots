import random

from lexicon.ru import LEXICON_RU


def get_bot_choise() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


def _normailize_user_answer(user_answer: str) ->str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            return key


def get_winner(user_choice: str, bot_choice: str):
    user_choice: str = _normailize_user_answer(user_choice)
    rules: dict[str, str] = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    if user_choice == bot_choice:
        return 'nobody_won'
    elif rules[user_choice] == bot_choice:
        return 'user_won'
    else:
        return 'bot_won'
