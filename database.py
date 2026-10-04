#load pdf
#split into chunks
#create the embeddings
#store into chroma

from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

loader = PyPDFLoader("document loaders/GRU.pdf")
docs = loader.load()


splitter = RecursiveCharacterTextSplitter(
   chunk_size = 100,
   chunk_overlap=10
)

chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
  documents=chunks,
  embedding=embedding_model,
  persist_directory="Chroma_db"
)

