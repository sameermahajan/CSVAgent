import streamlit as st
import pandas as pd
import sqlite3
import os

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="School DB Agent",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 School Database AI Agent")

st.write("""
Ask questions like:
- Who is the topper?
- Which subject has highest average?
- Show marks of Rahul
""")

# =========================================================
# CSV FILE PATHS
# =========================================================

STUDENTS_CSV = "students.csv"
SUBJECTS_CSV = "subjects.csv"
MARKS_CSV = "marks.csv"

# =========================================================
# CHECK FILES EXIST
# =========================================================

required_files = [
    STUDENTS_CSV,
    SUBJECTS_CSV,
    MARKS_CSV
]

missing_files = [
    f for f in required_files if not os.path.exists(f)
]

if missing_files:

    st.error(
        f"Missing CSV files: {missing_files}"
    )

    st.stop()

# =========================================================
# LOAD CSV FILES
# =========================================================

try:

    students_df = pd.read_csv(STUDENTS_CSV)
    subjects_df = pd.read_csv(SUBJECTS_CSV)
    marks_df = pd.read_csv(MARKS_CSV)

    st.success("✅ CSV files loaded automatically!")

except Exception as e:

    st.error(f"CSV loading error: {e}")
    st.stop()

# =========================================================
# CREATE SQLITE DATABASE
# =========================================================

try:

    conn = sqlite3.connect("school.db")

    students_df.to_sql(
        "students",
        conn,
        if_exists="replace",
        index=False
    )

    subjects_df.to_sql(
        "subjects",
        conn,
        if_exists="replace",
        index=False
    )

    marks_df.to_sql(
        "marks",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    st.success("✅ SQLite database created!")

except Exception as e:

    st.error(f"Database creation error: {e}")
    st.stop()

# =========================================================
# CONNECT LLM
# =========================================================

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="qwen2.5-coder:32b",
    temperature=0
)

# =========================================================
# CONNECT DATABASE
# =========================================================

db = SQLDatabase.from_uri(
    "sqlite:///school.db"
)

# =========================================================
# CREATE SQL CHAIN
# =========================================================

db_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    verbose=True,
    return_intermediate_steps=True
)

# =========================================================
# USER INPUT
# =========================================================

question = st.text_input(
    "Ask your question",
    placeholder="Who is the topper of class?"
)

# =========================================================
# QUERY EXECUTION
# =========================================================

if st.button("Submit"):

    if question.strip():

        with st.spinner("Thinking..."):

            PREFIX = """
You are an expert school database analyst.

DATABASE SCHEMA:

students:
- student_id
- student_name

subjects:
- subject_id
- subject_name

marks:
- student_id
- subject_id
- marks

RELATIONSHIPS:
- marks.student_id joins students.student_id
- marks.subject_id joins subjects.subject_id

IMPORTANT RULES:
- Always think step-by-step
- Always generate SQL first
- Use proper JOINs
- For topper:
    SUM marks grouped by student
- Return concise answers
"""

            final_prompt = f"""
{PREFIX}

QUESTION:
{question}
"""

            try:

                response = db_chain.invoke({
                    "query": final_prompt
                })

                # =========================================================
                # SHOW ANSWER
                # =========================================================

                st.subheader("✅ Answer")

                st.write(response["result"])

                # =========================================================
                # SHOW SQL DEBUG
                # =========================================================

                with st.expander("SQL Reasoning"):

                    st.write(response["intermediate_steps"])

            except Exception as e:

                st.error(f"Query error: {e}")