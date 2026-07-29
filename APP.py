import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (ex: OPENAI_API_KEY)
load_dotenv()

# Configuration Streamlit
st.title("📄 Chatbot RAG avec PDF")
st.markdown("Posez des questions sur vos documents PDF")

# Upload de PDF
uploaded_file = st.file_uploader("Téléchargez votre PDF", type="pdf")

if uploaded_file:
    # Sauvegarder le PDF temporairement
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Charger et découper le PDF
    loader = PyPDFLoader("temp.pdf")
    pages = loader.load_and_split()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(pages)
    
    # Créer les embeddings et la base vectorielle
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # Alternative: HuggingFaceEmbeddings()
    vector_db = FAISS.from_documents(chunks, embeddings)
    
    # Initialiser le LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff"
    )
    
    # Chat UI
    user_query = st.text_input("Posez votre question ici:")
    if user_query:
        answer = qa_chain.run(user_query)
        st.write("🤖 Réponse:")
        st.success(answer)