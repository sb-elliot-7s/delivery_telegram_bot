from typing import Iterable

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.utils import Input
from langchain_core.vectorstores import VectorStoreRetriever


class RAG:
    def __init__(self, llm_model, retriever: VectorStoreRetriever, prompt_template: str):
        self.prompt_template = prompt_template
        self.retriever = retriever
        self.llm_model = llm_model

    @property
    def llm(self):
        return self.llm_model

    @llm.setter
    def llm(self, model):
        self.llm_model = model

    def __get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate.from_template(template=self.prompt_template)

    @staticmethod
    def __format_docs(docs: Iterable) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    async def answer(self, question: Input) -> str:
        context_question = {
            "context": self.retriever | self.__format_docs,
            "question": RunnablePassthrough()
        }
        rag_chain = context_question | self.__get_prompt_template() | self.llm | StrOutputParser()
        return await rag_chain.ainvoke(input=question)
