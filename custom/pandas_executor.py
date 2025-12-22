import pandas as pd
from typing import Dict

def execute_plan(plan, dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Execute a validated QueryPlan using pandas.
    """

    # -------------------------
    # 1. Load base dataframe
    # -------------------------
    if not plan.tables:
        raise ValueError("No tables specified in plan")

    df = dfs[plan.tables[0]].copy()

    # -------------------------
    # 2. Apply joins
    # -------------------------
    if plan.joins:
        for join in plan.joins:
            left_table, left_col = join.left.split(".")
            right_table, right_col = join.right.split(".")

            df = df.merge(
                dfs[right_table],
                left_on=left_col,
                right_on=right_col,
                how=join.type
            )

    # -------------------------
    # 3. Group by + aggregation
    # -------------------------
    if plan.aggregations:
        agg_map = {}
        for col, func in plan.aggregations.items():
            _, col_name = col.split(".")
            agg_map[col_name] = func

        if plan.group_by:
            group_cols = [c.split(".")[1] for c in plan.group_by]
            df = (
                df.groupby(group_cols, as_index=False)
                .agg(agg_map)
            )
        else:
            df = df.agg(agg_map).to_frame().T

    # -------------------------
    # 4. Order by
    # -------------------------
    if plan.order_by:
        for order in reversed(plan.order_by):
            col = order.column.split(".")[-1]
            ascending = order.direction == "asc"
            df = df.sort_values(by=col, ascending=ascending)

    # -------------------------
    # 5. Limit
    # -------------------------
    if plan.limit:
        df = df.head(plan.limit)

    return df
