from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputInvoiceMessageContent, LabeledPrice

from db.dish import Dish
from db.base import dish_collection
from configs import settings

conversation_router = Router(name='converation_router')


@conversation_router.inline_query()
async def dishes_inline(inline_query: InlineQuery):
    dishes = await Dish(collection=dish_collection).get_dishes()
    photo_url = ('https://images.unsplash.com/photo-1706685838669-69d5dcb5ecae?q=80&w=2069&auto=format'
                 '&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
    results = [
        InlineQueryResultArticle(
            input_message_content=InputInvoiceMessageContent(
                title=dish.name,
                description=dish.description,
                payload=f'dish:{dish.id}',
                provider_token=settings.provider_token,
                currency='rub',
                prices=[LabeledPrice(label=dish.name, amount=int(dish.price))],
                suggested_tip_amounts=[5000, 6000, 7000, 10000],
                max_tip_amount=10000,
                photo_url=photo_url,
                photo_height=500,
                photo_width=500,
                need_phone_number=True,
                need_shipping_address=True,
                is_flexible=False,
            ),
            id=str(dish.id),
            title=dish.name,
            description=dish.description,
            thumbnail_url=photo_url,
            thumbnail_width=500,
            thumbnail_height=500,
        ) for dish in dishes
    ]
    await inline_query.answer(results=results, is_personal=True)
