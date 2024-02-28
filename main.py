import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

from ai.store import RetrieverService
from configs import settings
from routers.common_router import common_router
from routers.admin_router import admin_router
from routers.dish_router import dish_router
from routers.payment_router import payment_router
from routers.conversation_router import conversation_router


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_routers(common_router, admin_router, dish_router, payment_router, conversation_router)
    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.MARKDOWN_V2)
    await bot.delete_webhook(drop_pending_updates=True)
    retriever = RetrieverService(vectorstore=PineconeVectorStore(
        index_name=settings.pinecone_index_name, embedding=OllamaEmbeddings(model='gemma:2b')
    )).get_retriever()
    await dp.start_polling(bot, retriever=retriever)


if __name__ == '__main__':
    asyncio.run(main())
