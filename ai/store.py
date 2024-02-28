import os
from dataclasses import dataclass

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from configs import settings

os.environ['PINECONE_API_KEY'] = settings.pinecone_api_key


class StoreService:
    def __init__(self, loader: BaseLoader, embedding: Embeddings, vectorstore, chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        self.loader = loader
        self.embedding = embedding
        self.vectorstore = vectorstore
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_docs(self) -> list[Document]:
        return self.loader.load()

    def text_splitter(self) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return text_splitter.split_documents(documents=self.get_docs())

    async def save_in_vectorstore(self, splitt_documents: list[Document]):
        return await self.vectorstore.afrom_documents(
            documents=splitt_documents, embedding=self.embedding, index_name=settings.pinecone_index_name
        )

    async def save(self) -> None:
        await self.save_in_vectorstore(splitt_documents=self.text_splitter())

    async def add_new_documents(self, documents: list[Document]):
        await self.vectorstore.aadd_documents(documents=documents)


@dataclass
class RetrieverService:
    vectorstore: VectorStore | None = None

    def get_retriever(self, search_type: str = 'similarity', **kwargs) -> VectorStoreRetriever:
        if self.vectorstore is None:
            raise ValueError('Vectorstore was not defined')
        return self.vectorstore.as_retriever(search_type=search_type, search_kwargs=kwargs)
