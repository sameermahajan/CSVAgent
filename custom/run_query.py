# run_query.py

import pandas as pd
from schema_retriever import retrieve_schema
from planner import plan_query
from pandas_executor import execute_plan

import json
from planner_schema import QueryPlan

topper_of_my_class_plan = """{
  "tables": ["students", "marks"],
  "steps": [
    {
      "metrics": {"marks.marks": "sum"},
      "group_by": ["students.student_id"]
    }
  ],
  "sort_by": "marks.marks",
  "limit": 1
}"""

generated_plan = """{
  "tables": ["students", "marks"],
  "steps": [
    {
      "metrics": {"marks.marks": "max"},
      "group_by": ["marks.student_id"]
    },
    {
      "metrics": {"marks.marks": "max"}
    }
  ],
  "filters": null,
  "sort_by": null,
  "limit": null
}"""

def queryplan_from_string(s: str) -> QueryPlan:
    data = json.loads(s)
    return QueryPlan.model_validate(data)

# Load data
marks = pd.read_csv("marks.csv")
subjects = pd.read_csv("subjects.csv")
students = pd.read_csv("students.csv")

dataframes = {
    "marks": marks,
    "subjects": subjects,
    "students": students
}

def run_pipeline(question):
    schema_text = retrieve_schema(question)
    print("Schema is : ", schema_text)

    plan = plan_query(question, schema_text)
    print("Query Plan:", plan)

    # plan = queryplan_from_string(topper_of_my_class_plan)

    # plan = queryplan_from_string(generated_plan)
    result = execute_plan(plan, dataframes)
    print(result)

run_pipeline("Who is the top student of my class?")

run_pipeline("What are the top marks in each subject?")

run_pipeline("List top marks of every subject along with student name who scored it")