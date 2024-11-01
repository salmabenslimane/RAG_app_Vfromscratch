



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
       st.file_uploader('Upload your PDFs here')
       st.button('Analyse PDFs')

       




if __name__== '__main__':
    main()

