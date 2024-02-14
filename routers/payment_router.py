import uuid
from datetime import datetime

from aiogram import Router, types, Bot, F
from callback_datas.dish_callback_data import DishCallbackData
from db.base import dish_collection
from db.dish import Dish
from configs import settings
from db.base import payment_collection
from db.payment import Payment
from schemas.payment import CreateSuccessfulPaymentSchema

payment_router = Router(name='payment_router')


@payment_router.callback_query(DishCallbackData.filter())
async def pay(callback: types.CallbackQuery, bot: Bot, callback_data: DishCallbackData):
    await callback.answer()

    dish_result = await Dish(collection=dish_collection).get_dish(dish_id=callback_data.id)
    if dish_result.status_code == 404:
        return await callback.message.answer(text=dish_result.message)
    price = types.LabeledPrice(label=dish_result.dish.name, amount=int(dish_result.dish.price))
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=dish_result.dish.name,
        description=dish_result.dish.description,
        payload=f'dish:{callback_data.id}',
        start_parameter=str(uuid.uuid4()),
        photo_url='https://images.unsplash.com/photo-1706685838669-69d5dcb5ecae?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        photo_width=1000,
        photo_height=1000,
        provider_token=settings.provider_token,
        prices=[price],
        currency='rub',
        is_flexible=False,
        need_shipping_address=True,
        need_phone_number=True,
        suggested_tip_amounts=[5000, 6000, 7000, 10000],
        max_tip_amount=10000,
    )


@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    """проверка доступности товара, если доступно ok=True."""
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)


@payment_router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    await Payment(collection=payment_collection).save_payment(payment_data=CreateSuccessfulPaymentSchema(
        from_user=message.from_user, successful_payment=message.successful_payment, time_created=datetime.now()
    ))
    await message.answer(text='Вы оплатили товар')
