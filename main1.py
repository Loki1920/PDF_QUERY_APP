import os
import streamlit as st
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_parse import LlamaParse
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API keys for LlamaCloud and OpenAI
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the temporary directory exists
TEMP_DIR = "/tmp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Initialize global variables for query engine, vector store, and parsed PDF
query_engine = None
vector_store = None
storage_context = None
vector_store_index = None
parsed_pdf = None

# Streamlit interface for file upload
st.title("PDF Parsing and Query App")

# Check if the PDF is already uploaded and processed
if "parsed_pdf" not in st.session_state:
    st.session_state.parsed_pdf = None
    st.session_state.vector_store_index = None
    st.session_state.query_engine = None

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None and st.session_state.parsed_pdf is None:
    temp_pdf_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("File uploaded successfully.")

    # Step 2: Process the PDF using LlamaParse (only once)
    parsing_instruction = """ 
        
                            Document Parsing Instructions:

                            Sections to Extract:

                            Identify and extract the main sections listed in the Table of Contents (e.g., "Meeting Updates", "Performance Data", "SBA Multi-Strategy Fund", etc.).
                            For each section, extract the relevant subsections and their content, focusing on key information such as fund weightings, liquidity dates, and performance data.
                            Dates & Events:

                            Under "Group Meeting Tracker" and "Open Projects", extract all meeting dates, fund names, subjects, owners, and status updates. Group these details per meeting date in chronological order.
                            For "Open Client Projects", extract the Date Created, Deadline, Owner, Client, Subject, and Status fields for each project.
                            Fund Performance Data:

                            Extract fund names, dates (month/year), returns (monthly, YTD, TTM), and other performance metrics (e.g., Sharpe ratio, standard deviation) from the "Performance Data", "Returns Summary & Statistics", and "Composite Returns" sections.
                            Organize by fund name, with columns for monthly returns, annual returns, and performance indicators such as maximum drawdown and correlation to S&P 500.
                            Performance Metrics:

                            For each listed fund, extract detailed performance data (e.g., annualized returns, standard deviation, max drawdown, Sharpe ratio) and organize them in a tabular format.
                            New Funds & World Indices:

                            Extract the names of any new funds and track changes or updates under the "New Fund Tracking List".
                            Extract relevant performance data from the "World Indices" section and present it as a separate table with indices names and corresponding performance metrics.
                            General Guidelines:

                            Ensure that all financial data (e.g., returns, correlations, and Sharpe ratios) are formatted as numerical values with correct units.
                            Group information logically based on the fund or event for easy cross-reference.

                            """
    
    pdf_parser = LlamaParse(result_type="markdown", parsing_instruction=parsing_instruction, split_by_page=1, api_key=LLAMA_CLOUD_API_KEY)
    st.session_state.parsed_pdf = pdf_parser.load_data(temp_pdf_path)
    st.write("PDF parsed successfully.")

    # Step 3: Set up LanceDB vector store and index the document (only once)
    vector_store = LanceDBVectorStore(uri=os.path.join(TEMP_DIR, "lancedb_lamaindex"))
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    st.session_state.vector_store_index = VectorStoreIndex.from_documents(st.session_state.parsed_pdf, storage_context=storage_context)
    st.write("PDF indexed successfully.")

    # Step 4: Initialize Flag Embedding Reranker and Query Engine (only once)
    reranker = FlagEmbeddingReranker(top_n=5, model="BAAI/bge-reranker-large")
    st.session_state.query_engine = st.session_state.vector_store_index.as_query_engine(similarity_top_k=10, node_postprocessors=[reranker])
    st.write("Query engine is ready.")

# Streamlit interface for querying the PDF
if st.session_state.parsed_pdf is not None:
    query_input = st.text_input("Enter your query:")
    
    if st.button("Run Query") and query_input:
        if st.session_state.query_engine is None:
            st.error("No document indexed. Please upload a PDF first.")
        else:
            # Query the indexed document using the query engine stored in session state
            response = st.session_state.query_engine.query(query_input)
            st.write("Query Result:")
            st.write(response.response)
