from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_datas.dish_callback_data import DishCallbackData
from schemas.dish import DishSchema


def pay_keyboard(dish_data: DishSchema):
    builder = InlineKeyboardBuilder()
    builder.button(text='Купить', callback_data=DishCallbackData(id=str(dish_data.id)), pay=True)
    return builder.as_markup()
