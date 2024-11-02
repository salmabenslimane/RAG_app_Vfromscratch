import streamlit as st 
from dotenv import load_dotenv
import pdfplumber 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS




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

def get_text_chunks(text):  #change smth if you wanna read les analyses
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
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore
    

def main():
   load_dotenv() #link to secrets in .env

   #st.set_page_config(page_title='Hi, my name is KOJO', page_icon=':books:')
   #IDK WHY THIS LINE IS NOT WORKING

   st.header("Hi, my name is KOJO :books:")
   st.text_input("Ask about your pdf")

   with st.sidebar: 
       st.subheader('hhhhhhhhhhhhhhh')
       PDFs = st.file_uploader('Upload your PDFs here', accept_multiple_files=True)
       if st.button('Analyse PDFs'):
           with st.spinner("Analyzing..."): #spins while loading answers
               # Récuperer le texte des pdfs  
                raw_text = get_pdf_text(PDFs)
                st.write(raw_text)
               # text chunks
                chunks = get_text_chunks(raw_text)
                
               # vector base 

       




if __name__== '__main__':
    main()

