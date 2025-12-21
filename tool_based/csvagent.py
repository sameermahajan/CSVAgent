from langchain_community.embeddings import OllamaEmbeddings
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_ollama import ChatOllama

import pandas as pd
from pathlib import Path
from langchain_community.vectorstores import Chroma

def strip_markdown_code_fences(code: str) -> str:
    code = code.strip()

    if code.startswith("```"):
        # remove first line (``` or ```python)
        code = code.split("\n", 1)[1]

    if code.endswith("```"):
        code = code.rsplit("\n", 1)[0]

    return code.strip()

# ----------------------------
# Absolute path (must match build)
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = (BASE_DIR / "schema_chroma").resolve()

print("Loading Chroma from:", CHROMA_DIR)

# ----------------------------
# Embeddings
# ----------------------------
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# ----------------------------
# Load Chroma
# ----------------------------
db = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings
)

# ----------------------------
# Retrieval function
# ----------------------------
def retrieve_schema(question: str, k: int = 5) -> str:
    docs = db.similarity_search(question, k=k)
    return "\n".join(d.page_content for d in docs)

# ----------------------------
# Load CSVs
# ----------------------------
students = pd.read_csv("students.csv")
marks = pd.read_csv("marks.csv")

exec_python_tool = PythonAstREPLTool(
    locals={"pd": pd, "students": students, "marks": marks}
)

# ----------------------------
# LLM (ONE call only)
# ----------------------------
llm = ChatOllama(
    model="qwen2.5-coder:32b",
    temperature=0
)

# ----------------------------
# Run pipeline
# ----------------------------
question = "Who is the topper of the class?"

schema = retrieve_schema(question)

print("Schema is : ", schema)

prompt = f"""
You are a data analysis agent.

Schema information:
{schema}

Rules:
- Use ONLY pandas
- Do NOT explain anything

use 'student_id' as column name for students dataframe NOT 'id'

use unique identifiers for dataframes for groupby operations and any aggregations to avoid duplicates

Question:
{question}
"""

python_code = llm.invoke(prompt).content

print("Python code is : ", python_code)

python_code = strip_markdown_code_fences(python_code)

result = exec_python_tool.invoke(python_code)

print(result)
