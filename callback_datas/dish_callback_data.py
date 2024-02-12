from aiogram.filters.callback_data import CallbackData


class AdminDishCallbackData(CallbackData, prefix='dish'):
    action: str


class DishCallbackData(CallbackData, prefix='list_dish'):
    id: str
