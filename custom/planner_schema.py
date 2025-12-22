from typing import List, Dict, Optional
from pydantic import BaseModel

class Join(BaseModel):
    left: str
    right: str
    type: str

class OrderBy(BaseModel):
    column: str
    direction: str

class QueryPlan(BaseModel):
    tables: List[str]
    joins: Optional[List[Join]] = None
    group_by: Optional[List[str]] = None
    aggregations: Optional[Dict[str, str]] = None
    order_by: Optional[List[OrderBy]] = None
    limit: Optional[int] = None
