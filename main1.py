# file: app.py
import os
import streamlit as st
import nest_asyncio
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_parse import LlamaParse
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker



# Ensure async compatibility for notebook-like environments
nest_asyncio.apply()

# Set up API keys for LlamaCloud and OpenAI
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Streamlit App
st.title("PDF Query App")

# Step 1: Upload the PDF file
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded PDF file temporarily
    temp_pdf_path = f"/tmp/{uploaded_file.name}"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Step 2: Process the PDF using LlamaParse
    st.write("Processing the PDF...")
    pdf_parser = LlamaParse(result_type="markdown", split_by_page=1)
    parsed_pdf = pdf_parser.load_data(temp_pdf_path)

    # Step 3: Set up LanceDB vector store and index the document
    st.write("Indexing the document...")
    vector_store = LanceDBVectorStore(uri="/tmp/lancedb_lamaindex")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    vector_store_index = VectorStoreIndex.from_documents(parsed_pdf, storage_context=storage_context)

    # Step 4: Initialize Flag Embedding Reranker
    reranker = FlagEmbeddingReranker(top_n=5, model="BAAI/bge-reranker-large")
    
    # Step 5: Set up the query engine
    query_engine = vector_store_index.as_query_engine(similarity_top_k=10, node_postprocessors=[reranker])

    # Step 6: Get user query input
    query_input = st.text_input("Ask a question about the PDF:")

    if st.button("Run Query") and query_input:
        # Step 7: Query the indexed document
        st.write(f"Querying : {query_input}")
        response = query_engine.query(query_input)

        # Step 8: Display the result
        st.write("\n**********Response********** :")
        st.write(response.response)

else:
    st.write("Please upload a PDF file to get started.")
