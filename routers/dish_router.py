from aiogram import Router, types
from aiogram.filters import Command

from db.dish import Dish
from db.base import dish_collection
from keyboards.pay_keyboard import pay_keyboard
from utils.text_utils import get_caption_dish

dish_router = Router(name='dish_router')


@dish_router.message(Command('dishes'))
async def show_dishes(message: types.Message):
    dishes = await Dish(collection=dish_collection).get_dishes()
    for dish in dishes:
        caption: str = get_caption_dish(name=dish.name, description=dish.description, price=dish.price)
        await message.answer_photo(photo=dish.photo, caption=caption, reply_markup=pay_keyboard(dish_data=dish))
