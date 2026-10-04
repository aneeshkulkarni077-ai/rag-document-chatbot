# 🧠 RAG Document Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that answers questions from PDF documents using semantic search, vector embeddings, and a Large Language Model. The project uses **LangChain, Groq, Hugging Face Embeddings, ChromaDB, and Streamlit** to provide an interactive document question-answering experience.

> **🌐 LIVE Working Link:** [Open the deployed app](https://aneeshkulkarni077-ai-rag-document-chatbot-app-wufmfs.streamlit.app)

## 🌐 Live Application

🚀 **Try the project here:**

[Open RAG Document Chatbot](https://aneeshkulkarni077-ai-rag-document-chatbot-app-wufmfs.streamlit.app)
The application allows users to ask questions about document content and receive answers generated using relevant information retrieved from the uploaded or configured documents.

*Note: The live link will work once the application has been deployed.*

## 📌 Project Overview

Finding specific information in lengthy documents can be time-consuming. This project uses Retrieval-Augmented Generation (RAG) to make document-based question answering easier.

The application follows these steps:

* 📄 Loads PDF and text documents
* ✂️ Splits documents into smaller text chunks
* 🔢 Converts text chunks into numerical embeddings
* 🗄️ Stores embeddings in a ChromaDB vector database
* 🔍 Retrieves relevant information using semantic similarity search
* 🤖 Uses a Large Language Model to generate answers from retrieved context
* 💬 Provides an interactive Streamlit chat interface

The goal is to generate contextually relevant answers based on the information available in the documents.

## ✨ Features

* 📄 PDF document processing
* 📝 Text document loading
* ✂️ Recursive text splitting
* 🧠 Hugging Face sentence embeddings
* 🗄️ ChromaDB vector storage
* 🔍 Semantic similarity search
* 🤖 LLM-powered question answering
* ⚡ Groq API integration
* 💬 Interactive Streamlit interface
* 🖥️ Terminal-based chatbot
* 🔐 Environment variable support for API keys

## 🛠️ Tech Stack

### Programming Language

* Python

### LLM Integration

* LangChain
* Groq API
* `openai/gpt-oss-20b` model through Groq

### Embeddings

* Hugging Face Sentence Transformers
* `sentence-transformers/all-MiniLM-L6-v2`

### Vector Database

* ChromaDB

### Document Processing

* PyPDFLoader
* TextLoader
* RecursiveCharacterTextSplitter

### Frontend

* Streamlit

### Environment and Dependency Management

* uv
* python-dotenv

## 🧠 How RAG Works

The project follows a Retrieval-Augmented Generation workflow.

1. **Document Loading:** Reads the contents of PDF and text files.
2. **Text Splitting:** Divides the document into smaller chunks using a text splitter.
3. **Embedding Generation:** Converts text chunks into vector representations using a Hugging Face embedding model.
4. **Vector Storage:** Stores the embeddings in ChromaDB.
5. **Retrieval:** Searches the vector database for chunks relevant to the user's question.
6. **Answer Generation:** Sends the retrieved context and user's question to the language model.
7. **Response:** Displays the generated answer in the chatbot interface.

## 🔍 Vector Database

The project uses **ChromaDB** to store and search document embeddings.

Instead of passing an entire document to the language model for every question, the application retrieves relevant chunks from the vector database and uses them as context.

This helps the model answer questions based on the available document information.

## 📚 Document Processing

The application uses LangChain document loaders to read different types of files.

| Component                        | Purpose                                   |
| -------------------------------- | ----------------------------------------- |
| `PyPDFLoader`                    | Loads content from PDF documents          |
| `TextLoader`                     | Loads plain-text files                    |
| `RecursiveCharacterTextSplitter` | Splits documents into manageable chunks   |
| Hugging Face Embeddings          | Converts text into vector representations |
| ChromaDB                         | Stores and retrieves embeddings           |

The current text-splitting configuration uses a chunk size of **500 characters** and a chunk overlap of **100 characters**.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/aneeshkulkarni077-ai/rag-document-chatbot.git
cd rag-document-chatbot
```

### 2. Install uv

If you do not already have `uv` installed, follow the official installation instructions:

[Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### 3. Install project dependencies

Run the following command from the project directory:

```bash
uv sync
```

This installs the dependencies specified by the project's configuration and lock file.

### 4. Configure the environment variables

Create a `.env` file in the root project directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from the [Groq Console](https://console.groq.com/).

**Important:** Never upload your `.env` file or expose your API key publicly.

### 5. Run the Streamlit application

```bash
uv run streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the chatbot.

### 6. Run the terminal version

To run the command-line chatbot instead, use:

```bash
uv run python main.py
```

## 📁 Project Structure

```text
rag-document-chatbot/
│
├── document loaders/
│   ├── GRU.pdf
│   ├── notes.txt
│   ├── pdf.py
│   └── test.py
│
├── app.py
├── main.py
├── database.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

## 🔑 Environment Variables

The project uses environment variables to keep API credentials separate from the source code.

| Variable       | Purpose                                |
| -------------- | -------------------------------------- |
| `GROQ_API_KEY` | Authenticates requests to the Groq API |

Keep your API key private and configure it securely when deploying the application.

## ☁️ Deployment

The Streamlit application can be deployed using **Streamlit Community Cloud**.

Deployment platform: [Streamlit Community Cloud](https://share.streamlit.io/)

### Deployment Steps

1. Push the project to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Select the `rag-document-chatbot` repository.
4. Set `app.py` as the main application file.
5. Add `GROQ_API_KEY` under the app's Secrets settings.
6. Deploy the application.
7. Copy the generated public URL into the Live Application section of this README.

Ensure that document files are included where needed and that the vector database can be initialized or recreated in the deployment environment.

## 🔮 Future Improvements

* Support for uploading multiple PDF files
* Display retrieved source documents alongside answers
* Show page numbers for retrieved information
* Improved conversation history
* Support for additional document formats
* Better error handling and response validation
* Deployment with a public live demo

## ⚠️ Disclaimer

This project is intended for educational and learning purposes. The answers generated by the language model may occasionally be incomplete or inaccurate. Always verify important information against the original documents.

## 👨‍💻 Author

**Aneesh Kulkarni**

### 🔗 Project Links

* 🌐 **Live Demo:** Add your deployed Streamlit URL
* 💻 **GitHub Repository:** [rag-document-chatbot](https://github.com/aneeshkulkarni077-ai/rag-document-chatbot)
* ⚡ **Groq Console:** [Get API access](https://console.groq.com/)
* ☁️ **Streamlit Community Cloud:** [Deploy the application](https://share.streamlit.io/)

---

⭐ If you find this project useful, consider giving the repository a star!
