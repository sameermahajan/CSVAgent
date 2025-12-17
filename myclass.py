from langchain_experimental.agents.agent_toolkits import create_csv_agent

from langchain_openai import ChatOpenAI, OpenAI

llm = ChatOpenAI(base_url = 'http://localhost:11434/v1', 
                    api_key = 'ollama', 
                    model = 'llama2', 
                    temperature=0)

agent = create_csv_agent(
    llm,
    ["students.csv", "classes.csv", "marks.csv"],
    verbose=True,
    allow_dangerous_code=True,

    prefix = (
        "You are a CSV data analysis agent.\n"
        "You MUST use pandas to compute answers.\n"
        "When finished, respond EXACTLY as:\n"
        "Final Answer: <answer>\n"
        "Do not add extra text.\n"
        "Make sure you add up marks of all 5 subjects that every student is enrolled in.\n"
    ),

    # suffix = (
        # ---- Few-shot example 1 ----
    #    "Question: Who is the topper of the class?\n"
    #    "Final Answer: Danielle\n\n"

        # ---- Few-shot example 2 ----
    #    "Question: What are the top marks in Math?\n"
    #    "Final Answer: 98\n\n"

        # ---- Actual user input (REQUIRED) ----
    #    "Question: {input}\n"
    #    "Final Answer:"
    #),

    agent_executor_kwargs={
        "handle_parsing_errors": True
    }
)

# print (agent)

response = agent.invoke({"input": "Who is the topper of the class?"})
print(response["output"])

# print(agent.run("Who is the topper of my class?"))

# print(agent.run("what are the top marks in each subject?"))

# print(agent.run("list top marks of every subject along with student name who scored it"))
