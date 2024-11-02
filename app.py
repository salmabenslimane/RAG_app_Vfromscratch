import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader




def get_pdf_text(PDFs): #takes a list of pdf files and returns a str with all of the content 
   text =''
   for pdf in PDFs: #loop through pdfs uploaded
      pdf_reader = PdfReader(pdf) #creates an object with pages
      for page in pdf_reader.pages:
            text = page.extract_text()
   return text



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

               # vector base 

       




if __name__== '__main__':
    main()

