import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS



def get_pdf_text(PDFs): #takes a list of pdf files and returns a str with all of the content 
   text =''
   for pdf in PDFs: #loop through pdfs uploaded
      pdf_reader = PdfReader(pdf) #creates an object with pages
      for page in pdf_reader.pages:
            text = page.extract_text()
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
                
               # text chunks
                chunks = get_text_chunks(raw_text)
                st.write(chunks)
               # vector base 

       




if __name__== '__main__':
    main()

