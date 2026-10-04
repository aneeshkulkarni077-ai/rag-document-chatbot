from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
data = PyPDFLoader("document loaders/GRU.pdf")

docs = data.load()

splitter = RecursiveCharacterTextSplitter(
   chunk_size = 100,
   chunk_overlap=10
)

chunks = splitter.split_documents(docs)
print(chunks[0])
print()
print()
print()
for doc in docs:
    print("CONTENT:")
    print(doc.page_content)

    print("\nMETADATA:")
    print(doc.metadata)

    print("-" * 50)


