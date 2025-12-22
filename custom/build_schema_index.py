# build_schema_index.py

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from schema_registry import SCHEMA

embeddings = OllamaEmbeddings(model="nomic-embed-text")

docs = []
doc_id = 0
ids = []

for dataframe, meta in SCHEMA.items():
    docs.append(
        Document(
            page_content=f"dataframe {dataframe}: {meta['description']}",
            metadata={
                "type": "dataframe",
                "dataframe": dataframe
            }
        )
    )
    ids.append(str(doc_id))
    doc_id += 1

    for col, desc in meta["columns"].items():
        docs.append(
            Document(
                page_content=f"Column : {dataframe}.{col} : {desc}",
                metadata={
                    "type": "column",
                    "dataframe": dataframe,
                    "column": col
                }
            )
        )
        ids.append(str(doc_id))
        doc_id += 1

db = FAISS.from_documents(
    documents=docs,
    embedding=embeddings,
    ids=ids
)

db.save_local("schema_index")
