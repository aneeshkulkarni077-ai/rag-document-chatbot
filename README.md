

\# RAG Document Chatbot



This is a RAG-based chatbot that answers questions from PDF documents. It retrieves relevant information from the document and uses an LLM to generate answers through a Streamlit interface.



\## Tech Stack



\- Python

\- LangChain

\- Groq API

\- Hugging Face Embeddings

\- ChromaDB

\- Streamlit



\## How It Works



1\. Loads the PDF document.

2\. Splits the text into smaller chunks.

3\. Converts the chunks into embeddings.

4\. Stores the embeddings in ChromaDB.

5\. Retrieves relevant chunks based on the user's question.

6\. Uses the retrieved content to generate an answer.



\## Project Structure



```text

RAG project/

├── document loaders/

├── app.py

├── main.py

├── database.py

├── requirements.txt

├── pyproject.toml

├── uv.lock

├── .gitignore

└── README.md

```



\## Setup



Clone the repository and open the project folder.



```bash

git clone YOUR\_REPOSITORY\_URL

cd "RAG project"

```



Install the dependencies:



```bash

uv sync

```



Create a `.env` file in the project folder and add your Groq API key:



```env

GROQ\_API\_KEY=your\_groq\_api\_key

```



Run the Streamlit app:



```bash

uv run streamlit run app.py

```



To run the terminal version:



```bash

uv run python main.py

```



\## Current Features



\- PDF document loading

\- Text splitting and embedding generation

\- Semantic search using ChromaDB

\- Question answering using Groq

\- Streamlit chat interface



\## Future Improvements



\- Support for uploading multiple PDFs

\- Displaying source pages with answers

\- Improved chat history

\- Online deployment

