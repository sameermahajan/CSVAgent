# planner.py
import json
import re
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from planner_schema import QueryPlan
from schema_registry import ENTITY_KEYS

llm = ChatOllama(model="llama3.1", temperature=0)

# {{
#  "tables": ["table1", "table2"],
#  "step":
#    {{
#      "metrics": {{"table.column": "aggregation"}},
#      "group_by": ["table.column"] | null
#    }}
#  ,
#  "filters": null,
#  "sort_by": null,
#  "limit": null
#}}

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a query planner.

You MUST return ONLY valid JSON matching this schema:

{{
  "tables": ["table1", "table2"],
  "joins": [
    {{
      "left": "table1.column_name",
      "right": "table2.column_name",
      "type": "inner"
    }}
  ],
  "group_by": ["table1.column_name"],
  "aggregations": {{
    "table2.column_name": "aggregation"
  }},
  "order_by": [
    {{ "column": "table2.column_name", "direction": "desc" }}
  ],
  "limit": 1
}}

CRITICAL RULES:
- The JSON represents a SINGLE logical query plan
- Use AT MOST ONE aggregation block
- Ranking (top, highest, lowest) is expressed ONLY via group_by, aggregation by sum, order_by + limit
- group_by MUST be over a column representing unique values from a chosen table
- Do NOT invent multiple stages or steps
- Do NOT return SQL
- Do NOT explain
"""),
    ("human", """
Question:
{question}

Available schema:
{schema}
""")
])

def semantic_validate(plan: QueryPlan, question: str):
    q = question.lower()

    if "topper" in q or "highest total" in q:
        if plan.aggregations:
            agg = next(iter(plan.aggregations.values()))
            if agg != "sum":
                raise ValueError(
                    "Semantic error: 'topper' requires SUM aggregation"
                )

import json
import re

def parse_llm_json(text: str) -> dict:
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)

def plan_query(question: str, schema: str) -> QueryPlan:
    """
    Generates and validates a query plan using the LLM.

    Returns:
        QueryPlan (validated Pydantic model)

    Raises:
        ValueError / ValidationError if plan is invalid
    """

    print("inside plan_query")
    print("schema is : ", schema)
    print("question is : ", question)

    # 1. Invoke LLM
    response = llm.invoke(
        PROMPT.format_messages(
            question=question,
            schema=schema
        )
    )

    print("llm response is : ", response.content)

    # 2. Parse JSON
    try:
        plan_dict = parse_llm_json(response.content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM:\n{response.content}") from e

    # 3. Validate structure
    try:
        plan = QueryPlan.model_validate(plan_dict)
    except ValidationError as e:
        raise ValueError(f"Plan schema validation failed:\n{e}") from e

    # 4. Semantic validation (domain rules)
    semantic_validate(plan, question)

    return plan
