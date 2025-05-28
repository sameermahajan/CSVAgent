from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents import AgentType

from langchain_openai import ChatOpenAI, OpenAI
llm = ChatOpenAI(base_url = 'http://localhost:11434/v1', api_key='ollama', model = 'llama2')

agent = create_csv_agent(
    llm,
    ["students.csv", "classes.csv", "marks.csv"],
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True,
)

print(agent.run("Who is the topper of my class?"))

print(agent.run("what are the top marks in each subject?"))

print(agent.run("list top marks of every subject along with student name who scored it"))
