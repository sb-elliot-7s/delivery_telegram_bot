import asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from ai.store import StoreService
from configs import settings


async def load_documents():
    print('load documents ...')
    store_data = {
        'vectorstore': PineconeVectorStore,
        'loader': WebBaseLoader(web_path=[settings.document_url]),
        'embedding': OllamaEmbeddings(model='gemma:2b')
    }
    store_service = StoreService(**store_data)
    await store_service.save()
    print('save documents!')


if __name__ == '__main__':
    asyncio.run(load_documents())
