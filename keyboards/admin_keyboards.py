from .keyboard_builders import inline_keyboard_builder


def admin_keyboard():
    return inline_keyboard_builder(
        texts=['Добавить блюдо', 'Удалить блюдо', 'Статистика'],
        callback_datas=['add_good', 'delete_good', 'stats'],
        sizes=[3]
    )
