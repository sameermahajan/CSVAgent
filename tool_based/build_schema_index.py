from pathlib import Path
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from schema_registry import SCHEMA

# ----------------------------
# Absolute, stable path
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "schema_chroma"

# ----------------------------
# Embeddings
# ----------------------------
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# ----------------------------
# Build documents
# ----------------------------
docs = []

for dataframe, meta in SCHEMA.items():
    docs.append(
        Document(
            page_content=f"DataFrame {dataframe}: {meta['description']}",
            metadata={"type": "dataframe", "dataframe": dataframe}
        )
    )

    for col, desc in meta["columns"].items():
        docs.append(
            Document(
                page_content=f"Column {dataframe}.{col}: {desc}",
                metadata={
                    "type": "column",
                    "dataframe": dataframe,
                    "column": col
                }
            )
        )

# ----------------------------
# Create & persist Chroma
# ----------------------------
db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)

db.persist()

print("✅ Chroma schema index built at:", CHROMA_DIR)
