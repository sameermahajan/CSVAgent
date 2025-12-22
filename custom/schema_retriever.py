# schema_retriever.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

db = FAISS.load_local(
    "schema_index",
    embeddings,
    allow_dangerous_deserialization=True
)

def retrieve_schema(question, k=8):
    docs = db.similarity_search(question, k=k)
    return "\n".join(d.page_content for d in docs)
