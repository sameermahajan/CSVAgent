# langchain 0.1.17

from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_openai import ChatOpenAI
import pandas as pd

# Load data
students = pd.read_csv("students.csv")
subjects = pd.read_csv("subjects.csv")
marks = pd.read_csv("marks.csv")

python_tool = PythonAstREPLTool(
    locals={
        "students": students,
        "subjects": subjects,
        "marks": marks,
        "pd": pd
    }
)

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3.1",
    temperature=0
)

agent = initialize_agent(
    tools=[python_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

print(agent.run("Who is the topper of the class?"))
