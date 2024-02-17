from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import text, markdown_decoration

from keyboards.start_keyboards import start_keyboard
from db.user import UserDB
from db.base import user_collection

common_router = Router(name='common_router')


@common_router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user
    await UserDB(user_collection).save_user(user_document={'_id': user.id, **user.model_dump(exclude={'id'})})
    await message.answer_photo(
        photo='https://etimg.etb2bimg.com/photo/84847436.cms',
        caption=f'Данный бот поможет вам быстро выбрать блюдо, оплатить и получить ваш заказ',
        reply_markup=start_keyboard()
    )


@common_router.message(Command('help'))
async def help_handler(message: types.Message):
    await message.answer(text='help message')


@common_router.message(F.text == 'Показать контакты')
async def contacts_handler(message: types.Message):
    await message.reply(text=text(
        markdown_decoration.quote('Телефон: +89007773355\n\nEmail: sobaka@gmail.com\n\nhttps://delivery-food.com')))
