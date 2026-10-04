
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .stApp {
        background: #0D1117;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #111821;
        border-right: 1px solid #263241;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 1.5rem 0 1rem 0;
    }

    .hero h1 {
        color: #F0F6FC;
        font-size: 2.3rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #9BA9B9;
        font-size: 1rem;
    }

    .stChatMessage {
        background: #141B24;
        border: 1px solid #263241;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    [data-testid="stChatInput"] {
        border-color: #344255;
    }

    .status {
        background: #142B24;
        color: #76D9A4;
        padding: 0.55rem 0.8rem;
        border-radius: 8px;
        font-size: 0.85rem;
        margin: 0.7rem 0 1rem 0;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #263241;
        border-radius: 10px;
    }

    .stCaption {
        color: #9BA9B9;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Preparing your RAG system...")
def initialize_rag():
    # Load PDF
    loader = PyPDFLoader("document loaders/GRU.pdf")
    documents = loader.load()

    # Split PDF into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    # Initialize embeddings
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Open or create persistent Chroma database
    vectorstore = Chroma(
        collection_name="gru_documents",
        embedding_function=embedding_model,
        persist_directory="Chroma_db_streamlit"
    )

    # Index documents only if the collection is empty
    if vectorstore._collection.count() == 0:
        vectorstore.add_documents(chunks)

    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    # Initialize Groq LLM
    llm = init_chat_model(
        model="openai/gpt-oss-20b",
        model_provider="groq",
        temperature=0
    )

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a helpful RAG assistant.

Answer the user's question using the provided context.
Combine relevant information from multiple passages when needed.
If the answer cannot be found in the context, say:
"I don't know based on the provided context."

Do not invent facts. Explain answers clearly."""
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}"""
        )
    ])

    return retriever, prompt, llm


# Sidebar
with st.sidebar:
    st.markdown("## 🧠 RAG Assistant")
    st.caption("Retrieval-Augmented Generation")

    st.divider()

    st.markdown("### Your knowledge base")
    st.markdown("📄 **GRU.pdf**")
    st.caption("Source: Romain Tavenard's document")

    st.divider()

    st.markdown("### Configuration")
    st.markdown("**LLM:** Groq")
    st.markdown("**Embeddings:** MiniLM")
    st.markdown("**Vector store:** ChromaDB")
    st.markdown("**Retrieval:** Similarity Search")

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Answers are generated from retrieved document context.")


# Main page
st.markdown("""
<div class="hero">
    <h1>Chat with your documents</h1>
    <p>Ask questions about your PDF and get context-based answers.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="status">● RAG assistant ready</div>',
    unsafe_allow_html=True
)

# Initialize RAG components
try:
    retriever, prompt, llm = initialize_rag()
except Exception as error:
    st.error(
        "Could not initialize the RAG system. "
        "Check your PDF path, installed packages, and API key."
    )
    with st.expander("Technical details"):
        st.code(str(error))
    st.stop()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Welcome screen
if not st.session_state.messages:
    st.markdown("### 👋 Welcome!")
    st.write("Start with one of these questions:")

    suggestions = [
        "What does GRU stand for?",
        "What is the role of the update gate in a GRU?",
        "Which gates are present in a Gated Recurrent Unit?"
    ]

    columns = st.columns(3)

    for index, suggestion in enumerate(suggestions):
        with columns[index]:
            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True
            ):
                st.session_state.pending_query = suggestion
                st.rerun()


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 View retrieved sources"):
                for source in message["sources"]:
                    st.markdown(source)


# Chat input
query = st.chat_input("Ask anything about your documents...")

# Handle suggested questions
if "pending_query" in st.session_state:
    query = st.session_state.pop("pending_query")


if query:
    query = query.strip()

    if query:
        # Display user message
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.markdown(query)

        # Retrieve and generate answer
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer..."):
                try:
                    retrieved_docs = retriever.invoke(query)

                    context = "\n\n".join(
                        doc.page_content for doc in retrieved_docs
                    )

                    if not context.strip():
                        answer = (
                            "I couldn't retrieve relevant information "
                            "from the document for this question."
                        )
                    else:
                        messages = prompt.invoke({
                            "context": context,
                            "question": query
                        })

                        response = llm.invoke(messages)
                        answer = response.content

                    st.markdown(answer)

                    # Collect source information
                    sources = []

                    for doc in retrieved_docs:
                        source = doc.metadata.get("source", "Unknown source")
                        page = doc.metadata.get("page")

                        if page is not None:
                            source_text = f"📄 {source} — Page {page + 1}"
                        else:
                            source_text = f"📄 {source}"

                        if source_text not in sources:
                            sources.append(source_text)

                    if sources:
                        with st.expander("📚 View retrieved sources"):
                            for source in sources:
                                st.markdown(source)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as error:
                    st.error("Something went wrong while generating the answer.")
                    with st.expander("Technical details"):
                        st.code(str(error))