from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.utils.markdown import bold, text, markdown_decoration

from filters.is_admin import IsAdmin
from keyboards.admin_keyboards import admin_keyboard
from states.admin import AddDishState, DeleteDishState

admin_router = Router(name='admin_router')


@admin_router.message(Command('admin'), IsAdmin())
async def admin_routers(message: types.Message):
    await message.answer(text='Доступные команды:', reply_markup=admin_keyboard())


# ---- add dish -----

@admin_router.callback_query(F.data == 'add_good', IsAdmin(), default_state)
async def add_dish(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text='Введите название блюда')
    await state.set_state(AddDishState.name)


@admin_router.message(AddDishState.name, IsAdmin(), F.text)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Хорошо, теперь напишите описание блюда')
    await state.set_state(AddDishState.description)


@admin_router.message(AddDishState.description, IsAdmin(), F.text)
async def set_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text='Добавьте фото')
    await state.set_state(AddDishState.photo)


@admin_router.message(F.photo, AddDishState.photo, IsAdmin())
async def set_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer(text='Фото добавлено, последний шаг - установите цену')
    await state.set_state(AddDishState.price)


@admin_router.message(F.text, AddDishState.price, IsAdmin())
async def set_price(message: types.Message, state: FSMContext):
    if (price := message.text) and not price.isdigit():
        await message.answer(text='Цена должна состоять из цифр. Напишите цену')
        return
    await state.update_data(price=price)
    await message.answer(text='Блюдо успешно добавлено ✅')
    data = await state.get_data()
    caption = text(
        bold(data.get("name")),
        text(markdown_decoration.quote(data.get("description")),
             markdown_decoration.quote(f'{data.get("price")} руб.'), sep='\n'),
        sep='\n\n'
    )
    await message.answer_photo(photo=data.get('photo'), caption=caption, parse_mode=ParseMode.MARKDOWN_V2)
    """save dish in db"""
    await state.clear()


# ---- delete dish ----

@admin_router.callback_query(F.data == 'delete_good', IsAdmin(), default_state)
async def delete_good(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text='Введите id блюда')
    await state.set_state(DeleteDishState.dish_id)


@admin_router.message(IsAdmin(), DeleteDishState.dish_id, F.text)
async def delete_dish(message: types.Message, state: FSMContext):
    # await state.update_data(dish_id=message.text)
    """delete dish from db"""
    await message.reply(text='Блюдо было удалено ❌')
    await state.clear()


# ---- stats ----

@admin_router.callback_query(F.data == 'stats', IsAdmin())
async def stats(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(text='stats')
