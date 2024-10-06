import streamlit as st
import textwrap
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from generate_module import RailsDocOllama
#from htmlTemplates import css, bot_template, user_template

def main():
    load_dotenv()
    st.set_page_config(page_title="Ruby on Rails API Documentation Assistant", page_icon="💎", layout="wide")
    st.title("Ruby on Rails API Documentation Assistant")

    # Initialize the model and searcher
    @st.cache_resource
    def load_model_and_searcher():
        rag_rails = RailsDocOllama()
        return rag_rails

    model, searcher, llm = load_model_and_searcher()

    user_question = st.text_input("Ask a question about Ruby on Rails API:")

    if user_question:
        with st.spinner("Searching for relevant information..."):
            results = rag_rails.retrieve_answers(user_question)

            st.subheader("AI-generated Answer:")
            response = rag_rails.generate_answer(user_question)
            st.write("Based on the retrieved information, here's a summary of the answer to your question:")
            st.write(response)

            st.subheader("Relevant Information:")
            for i, result in enumerate(results, 1):
                with st.expander(f"Result {i}"):
                    st.markdown(textwrap.fill(result, width=80))

    st.sidebar.title("About")
    st.sidebar.info(
        "This app uses RAG (Retrieval-Augmented Generation) to provide "
        "information about the Ruby on Rails API. Ask a question, and it will "
        "search through indexed documentation to find relevant information."
    )
    st.sidebar.title("Tips")
    st.sidebar.info(
        "- Be specific in your questions\n"
        "- Try asking about specific Rails classes, methods, or concepts\n"
        "- If you don't get a satisfactory answer, try rephrasing your question"
    )

if __name__ == '__main__':
    main()
