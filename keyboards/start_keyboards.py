from .keyboard_builders import reply_keyboard_builder


def start_keyboard():
    return reply_keyboard_builder(
        texts=['Показать контакты', 'Поиск', 'Меню'],
        sizes=[2, 1],
        resize_keyboard=True
    )
