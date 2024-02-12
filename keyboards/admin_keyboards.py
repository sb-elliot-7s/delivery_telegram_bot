from callback_datas.dish_callback_data import AdminDishCallbackData
from .keyboard_builders import inline_keyboard_builder


def admin_keyboard():
    return inline_keyboard_builder(
        texts=['Добавить блюдо', 'Удалить блюдо', 'Статистика'],
        callback_datas=[
            AdminDishCallbackData(action='add').pack(),
            AdminDishCallbackData(action='delete').pack(),
            'stats'
        ],
        sizes=[2, 1]
    )
