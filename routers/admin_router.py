from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.utils.markdown import bold, text, markdown_decoration

from db.dish import Dish
from filters.is_admin import IsAdmin
from keyboards.admin_keyboards import admin_keyboard, DishCallbackData
from schemas.dish import DishSchema
from states.admin import AddDishState, DeleteDishState, set_first_state, update_state
from db.base import dish_collection

admin_router = Router(name='admin_router')


@admin_router.message(Command('admin'), IsAdmin())
async def admin_routers(message: types.Message):
    await message.answer(text='Доступные команды:', reply_markup=admin_keyboard())


# ---- add dish -----


def get_caption_dish(name: str, description: str, price: str):
    return text(
        bold(name),
        text(markdown_decoration.quote(description),
             markdown_decoration.quote(f'{price} руб.'), sep='\n'),
        sep='\n\n'
    )


@admin_router.callback_query(DishCallbackData.filter(F.action == 'add'), IsAdmin(), default_state)
async def add_dish(callback: types.CallbackQuery, state: FSMContext):
    await set_first_state(callback_message=callback, state=state, message_text='Введите название блюда',
                          first_state=AddDishState.name)


@admin_router.message(AddDishState.name, IsAdmin(), F.text)
async def set_name(message: types.Message, state: FSMContext):
    await update_state(state=state, message=message, message_state_data=message.text,
                       msg='Хорошо, теперь напишите описание блюда', next_state=AddDishState.description, key='name')


@admin_router.message(AddDishState.description, IsAdmin(), F.text)
async def set_description(message: types.Message, state: FSMContext):
    await update_state(state=state, message=message, message_state_data=message.text, msg='Добавьте фото',
                       next_state=AddDishState.photo, key='description')


@admin_router.message(F.photo, AddDishState.photo, IsAdmin())
async def set_photo(message: types.Message, state: FSMContext):
    await update_state(state=state, message=message, message_state_data=message.photo[-1].file_id, key='photo',
                       msg=text(markdown_decoration.quote('Фото добавлено, последний шаг - установите цену')),
                       next_state=AddDishState.price)


@admin_router.message(F.text, AddDishState.price, IsAdmin())
async def set_price(message: types.Message, state: FSMContext):
    if (price := message.text) and not price.isdigit() or float(price) <= 0.0:
        return await message.answer(text=text(markdown_decoration.quote(
            'Цена должна состоять из цифр и не может быть меньше 0.0. Напишите цену')))
    await state.update_data(price=price)
    await message.answer(text='Блюдо успешно добавлено ✅')
    dish_data = DishSchema(**await state.get_data())
    await Dish(collection=dish_collection).save_dish(dish_document=dish_data.model_dump())
    caption = get_caption_dish(**dish_data.model_dump(exclude={'photo'}))
    await message.answer_photo(photo=dish_data.photo, caption=caption)
    await state.clear()


# ---- delete dish ----

@admin_router.callback_query(DishCallbackData.filter(F.action == 'delete'), IsAdmin(), default_state)
async def delete_good(callback: types.CallbackQuery, state: FSMContext):
    await set_first_state(
        callback_message=callback, state=state, message_text='Введите id блюда', first_state=DeleteDishState.dish_id)


@admin_router.message(IsAdmin(), DeleteDishState.dish_id, F.text)
async def delete_dish(message: types.Message, state: FSMContext):
    # await state.update_data(dish_id=message.text)
    result = await Dish(collection=dish_collection).delete_dish(dish_id=message.text)
    if result:
        await message.reply(text='Блюдо было удалено ❌')
        await state.clear()
    else:
        await message.reply(text='Блюдо не найдено, повторите пожалуйста')


# ---- stats ----

@admin_router.callback_query(F.data == 'stats', IsAdmin())
async def stats(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='stats')
