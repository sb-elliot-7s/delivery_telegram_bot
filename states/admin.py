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


async def __common_set_state(message: types.Message, state: FSMContext, step: State, msg: str):
    await message.answer(text=msg)
    await state.set_state(step)


async def update_state(state: FSMContext, message: types.Message, message_state_data: str, msg: str, next_state: State,
                       key):
    await state.update_data({key: message_state_data})
    await __common_set_state(message=message, state=state, step=next_state, msg=msg)


async def set_first_state(callback_message: types.CallbackQuery, state: FSMContext, first_state: State,
                          message_text: str):
    await callback_message.answer()
    await __common_set_state(message=callback_message.message, state=state, step=first_state, msg=message_text)
