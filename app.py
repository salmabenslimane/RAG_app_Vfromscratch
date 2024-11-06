import streamlit as st 
from dotenv import load_dotenv, find_dotenv
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
    llm = HuggingFaceHub(repo_id="describeai/gemini",
                          model_kwargs={"temperature":0.7, "max_length":512},
                          huggingfacehub_api_token="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")
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation


def handle_userinput(user_question, conversation):
    response = conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

   
def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    load_dotenv()
    st.write(css, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
if __name__== '__main__':
    main()

