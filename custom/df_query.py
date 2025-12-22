import json
import re
import pandas as pd
from schema_retriever import retrieve_schema
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from planner_schema import QueryPlan, AggregationStep
from schema_registry import ENTITY_KEYS

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a pandas dataframe query generator.

You MUST return ONLY valid pandas dataframe queries.

Question:
{question}

Available schema:
{schema}
""")
])

def strip_markdown_code_fences(code: str) -> str:
    code = code.strip()

    if code.startswith("```"):
        # remove first line (``` or ```python)
        code = code.split("\n", 1)[1]

    if code.endswith("```"):
        code = code.rsplit("\n", 1)[0]

    return code.strip()

def generate_df_query(question: str, schema_text: str) -> str:
    # Call LLM
    response = llm.invoke(
        PROMPT.format_messages(
            question=question,
            schema=schema_text
        )
    )

    return response.content

# Load data
marks = pd.read_csv("marks.csv")
subjects = pd.read_csv("subjects.csv")
students = pd.read_csv("students.csv")

dataframes = {
    "marks": marks,
    "subjects": subjects,
    "students": students
}

llm = ChatOllama(model="qwen2.5-coder:32b", temperature=0)

question = "Who is the topper of my class?"

schema_text = retrieve_schema(question)
print("Schema is : ", schema_text)
query = generate_df_query(question, schema_text)
print("Query is : ", query)

from langchain_experimental.tools.python.tool import PythonAstREPLTool

# Python execution tool
python_tool = PythonAstREPLTool(
    locals={
        "pd": pd,
        "students": students,
        "marks": marks
    }
)

print('running python tool')
print(python_tool.run(query))

# import pandas as pd

# execution context
# globals_dict = {
#     "pd": pd,
#     "students": students,
#     "marks": marks
# }

# locals_dict = {}

# exec(strip_markdown_code_fences(query), globals_dict, locals_dict)

# retrieve result
# topper_df = locals_dict["topper_df"]
# print(topper_df)