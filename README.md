# ChatwithPDF_Vfromscratch
Building the pdfs chatbot from scratch with streamlit x huggingface LLM, without a starting template :) 


Logic of the app: 
PDFs --->  Chunks of text --->  Embeddings --- > Embedding vector database (pinecone, faissu ...) --- > Ranked results of the semantic search --- > LLM --- > Answer 


text chunks level (problems):
- deployement on streamlit 
- instructor for embeddings works good (check commit history)
- LLM?