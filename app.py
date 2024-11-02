import streamlit as st 
from dotenv import load_dotenv
import pdfplumber 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from htmlTemplates import css, bot_template, user_template


def get_pdf_text(PDFs):
    # Takes a list of PDF files and returns a string with all of the content
    text = ''
    for pdf in PDFs:  # loop through the uploaded PDFs
        with pdfplumber.open(pdf) as pdf_reader:
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"  # adding a newline for each page
    return text


def get_text_chunks(text):  
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# pip install InstructorEmbedding sentence_transformers (before)
def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings) #problem with faissu while deploying
    return vectorstore
    
#go back to this one ;)
def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key= 'chat history', return_messages= True)
    LLM = HuggingFaceHub(repo_id="microsoft/Phi-3.5-mini-instruct", model_kwargs={"temperature":0.7, "max_length":512})
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=LLM,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def main():
   
   load_dotenv() #link to secrets in .env

   if "conversation" not in st.session_state:
        st.session_state.conversation = None
   if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    #if the conversation chain and the memory of the chatbot are already initialized, it doesn't do anyth to them when refreshing


   st.set_page_config(page_title='Kojo, medical assistant ', page_icon=':books:')
   st.header("Hi, my name is Kojo :books:")
   st.subheader('Designed to help with medical results!')
   st.text_input("Upload your medical results")

   with st.sidebar: 
       st.subheader('Made by Salma Benslimane')
       PDFs = st.file_uploader('Upload your PDFs here', accept_multiple_files=True)
       if st.button('Analyse PDFs'):
           with st.spinner("Analyzing..."): #spins while loading answers
               # Récuperer le texte des pdfs  
                raw_text = get_pdf_text(PDFs)
                
               # text chunks
                text_chunks = get_text_chunks(raw_text)
                
               # vector base 
                vectorstore = get_vectorstore(text_chunks)

                #conversation and retrieval
                conversation_chain = get_conversation_chain(vectorstore) #st.session_state.concersation if you want variable to not be initialized everytime with streamlit


if __name__== '__main__':
    main()

