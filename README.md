# PDF_QUERY_APP


## Overview
The **PDF Query App** is a powerful Streamlit-based application that allows users to upload PDF files and extract information through natural language queries. It leverages advanced AI-powered libraries, such as LlamaIndex, OpenAI, and LanceDB, to efficiently index and query PDF documents. The app is especially useful for retrieving specific data points, summaries, and insights from complex PDF reports.

## Features
- Upload and process PDF files for text extraction.
- Run natural language queries to extract relevant information from PDFs.
- Utilizes LlamaIndex for document parsing and LanceDB for vector storage.
- Integrates OpenAI embeddings and FlagEmbedding Reranker for improved query relevance.

## Requirements
- **Python 3.8+**
- Required Python packages:
  - `llama-index`
  - `llama-index-core`
  - `llama-parse`
  - `streamlit`
  - `lancedb`
  - `unstructured`
  - `nest_asyncio`
  - `langchain`
  - `langchain-openai`

You can install all dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/PDF_QUERY_APP.git
   cd PDF_QUERY_APP
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   Install the required libraries using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables:**
   Create a `.env` file in the root directory of the project and add your API keys:
   ```
   OPENAI_API_KEY=your-openai-key
   LLAMA_CLOUD_API_KEY=your-llama-cloud-key
   ```

5. **Run the Streamlit App:**
   Launch the Streamlit app by running:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the app in your browser using the local URL provided by Streamlit.
2. Upload a PDF document.
3. Type a question about the document (e.g., "What is the financial summary?").
4. The app will process the query and return relevant information from the PDF.

## Folder Structure
```
PDF_QUERY_APP/
│
├── app.py                   # Main Streamlit app file
├── main.py                  # Core logic for PDF processing and querying
├── requirements.txt         # List of dependencies
├── .env                     # API keys (not tracked by Git)
└── README.md                # Project documentation
```

## Contributing
Feel free to contribute to the project by forking the repository and creating a pull request. Please ensure that your contributions are well-documented and thoroughly tested.

## License
This project is licensed under the MIT License.

---

**Next Steps**:
**a.** You might want to update the GitHub repository URL if you have not created it yet.
**b.** Consider adding screenshots of the app to make the README more informative.
