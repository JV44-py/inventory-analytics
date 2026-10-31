import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
eng = create_engine(os.getenv("DATABASE_URL"))

queries = {
    "Lost sales %": "SELECT ROUND(100.0 * SUM(demand_qty - sales_qty) / SUM(demand_qty), 2) AS lost_sales_pct FROM inv.stock_movements",
    "SKUs with under-buffered trigger": "SELECT COUNT(*) FILTER (WHERE p.base_demand * p.lead_time_days * 1.1 < r.reorder_point) AS under_buffered, COUNT(*) AS total_skus FROM inv.products p JOIN inv.reorder_analysis r USING (sku)",
    "Overstock": "SELECT COUNT(*) AS overstock_skus, ROUND(SUM(r.on_hand * p.unit_cost)) AS overstock_value FROM inv.reorder_analysis r JOIN inv.products p USING (sku) WHERE r.status = 'OVERSTOCK'",
    "ABC split": "SELECT abc_class, COUNT(*) AS skus FROM inv.v_abc GROUP BY abc_class ORDER BY abc_class",
}

for name, sql in queries.items():
    print(name)
    print(pd.read_sql(sql, eng).to_string(index=False))
    print()