from aiogram.filters.callback_data import CallbackData

from .keyboard_builders import inline_keyboard_builder


class DishCallbackData(CallbackData, prefix='dish'):
    action: str


def admin_keyboard():
    return inline_keyboard_builder(
        texts=['Добавить блюдо', 'Удалить блюдо', 'Статистика'],
        callback_datas=[
            DishCallbackData(action='add').pack(),
            DishCallbackData(action='delete').pack(),
            'stats'
        ],
        sizes=[2, 1]
    )
