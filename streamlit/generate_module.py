from sentence_transformers import SentenceTransformer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from openai import OpenAI
from rails_doc_es_index import RailsDocESIndex

TEMPLATE = """
You are an expert in Ruby on Rails. The user has asked a question regarding Ruby on Rails, and below is a list of relevant information retrieved from a knowledge base. Your goal is to generate a precise, well-explained response that addresses the user's question comprehensively, utilizing the details in the retrieved documents.

User Question: {question}

Retrieved Context:
{answers}

Instructions:

Use the information from the retrieved documents to generate a complete and detailed response to the user's question.
If any important concept or detail is missing from the retrieved context, provide general best practices in Ruby on Rails API development to fill in the gaps.
Your response should be clear and concise, focusing on solving the user's question while ensuring all technical aspects are easy to follow.
"""

class RailsDocOllama:
    def __init__(self):
        self.indexer = RailsDocESIndex()
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.llm = ChatOllama(
            model="gemma:2b",
            base_url="http://localhost:11434/"
        )
        self.prompt = self.prompt_template()

    def prompt_template(self):
        return ChatPromptTemplate.from_template(TEMPLATE)

    def retrieve_answers(self, question):
        query_embedding = self.embed_model.encode([question])[0]
        results = self.indexer.search(query_embedding, top_k=10)
        answers = "\n".join([f"Result 1: {r}" for r in results])
        return answers

    def generate_answer(self, question):
        llm_chain = self.prompt | self.llm
        response = llm_chain.invoke({
            "question": question,
            "answers": self.retrieve_answers(question)
        })
        return response.content

class RailsDocOpenAI:
    def __init__(self):
        self.indexer = RailsDocESIndex()
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.llm = OpenAI(
            base_url='http://localhost:11434/v1/',
            api_key='ollama',
        )

    def retrieve_answers(self, question):
        query_embedding = self.embed_model.encode([question])[0]
        results = self.indexer.search(query_embedding, top_k=10)
        answers = "\n".join([f"Result 1: {r}" for r in results])
        return answers

    def generate_answer(self, question):
        answers = self.retrieve_answers(question)
        prompt = TEMPLATE.format(question=question, answers=answers)
        response = self.llm.chat.completions.create(
            model='gemma:2b',
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
