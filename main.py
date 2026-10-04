
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Load PDF
data = PyPDFLoader("document loaders/GRU.pdf")
docs = data.load()

# Initialize LLM
llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="groq",
    temperature=0
)

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

# Create embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create a fresh vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="Chroma_db"
)

# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant for a RAG application.

Answer the question using the provided context.
Combine information from multiple passages when necessary.
If the answer cannot be found in the context, say:
"I don't know based on the provided context."

Do not invent information. Give a clear and accurate answer."""),

    ("human", """Context:
{context}

Question:
{question}""")
])

# Start RAG system
print("RAG system created!")
print("Ask questions about the GRU PDF.")
print("Press 0 to exit.\n")

while True:
    query = input("You: ").strip()

    if query == "0":
        print("RAG system stopped. Goodbye!")
        break

    if not query:
        print("Please enter a question.\n")
        continue

    # Retrieve relevant document chunks
    retrieved_docs = retriever.invoke(query)

    # Combine retrieved text into context
    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    # Debug: inspect retrieved context
    print("\n--- Retrieved Context ---")
    print(context if context else "No relevant documents retrieved.")
    print("-------------------------")

    # Format prompt with context and question
    messages = prompt.invoke({
        "context": context,
        "question": query
    })

    # Generate answer
    response = llm.invoke(messages)

    print("\nAI:", response.content)
    print()