



import streamlit as st 
from dotenv import load_dotenv


def main():
   load_dotenv()

   #st.set_page_config(page_title='Hi, my name is KOJO', page_icon=':books:')
   #IDK WHY THIS LINE IS NOT WORKING

   st.header("Hi, my name is KOJO :books:")
   st.text_input("Ask about your pdf")

   with st.sidebar: 
       st.subheader('hhhhhhhhhhhhhhh')
       PDFs = st.file_uploader('Upload your PDFs here', accept_multiple_files=True)
       if st.button('Analyse PDFs'):
           with st.spinner("Analyzing...") #spins while loading answers 
               # Récuperer le texte des pdfs

               # text chunks

               # vector base 

       




if __name__== '__main__':
    main()

