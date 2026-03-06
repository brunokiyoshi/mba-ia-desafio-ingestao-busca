import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")


def ingest_pdf():
    loader = PyPDFLoader(file_path=PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, add_start_index=False
    )

    chunks = splitter.split_documents(docs)

    for c in chunks:
        print(c)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)},
        )
        for d in chunks
    ]

    ids = [f"doc-{i}" for i in range(len(chunks))]

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        use_jsonb=True,
        connection=os.getenv("DATABASE_URL"),
    )

    store.add_documents(enriched, ids=ids)

if __name__ == "__main__":
    ingest_pdf()
