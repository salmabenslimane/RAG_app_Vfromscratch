



import streamlit as st 
def main():
   #st.set_page_config(page_title='Hi, my name is KOJO', page_icon=':books:')
   st.header("Hi, my name is KOJO :books:")
   st.text_input("Ask about your pdf")

   with st.sidebar: 
       st.subheader('hhhhhhhhhhhhhhh')
       st.file_uploader('Upload your PDFs here')

       




if __name__== '__main__':
    main()

