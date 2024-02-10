from aiogram.fsm.state import StatesGroup, State


class AddDishState(StatesGroup):
    name = State()
    description = State()
    photo = State()
    price = State()


class DeleteDishState(StatesGroup):
    dish_id = State()
