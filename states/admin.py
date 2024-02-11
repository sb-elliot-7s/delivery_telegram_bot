from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class AddDishState(StatesGroup):
    name = State()
    description = State()
    photo = State()
    price = State()


class DeleteDishState(StatesGroup):
    dish_id = State()


async def update_state(state: FSMContext, message: types.Message, message_state_data: str, msg: str, next_state: State,
                       key):
    await state.update_data({key: message_state_data})
    await message.answer(text=msg)
    await state.set_state(next_state)


async def set_first_state(callback_message: types.CallbackQuery, state: FSMContext, first_state: State,
                          message_text: str):
    await callback_message.answer()
    await callback_message.message.answer(text=message_text)
    await state.set_state(first_state)
