import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
eng = create_engine(os.getenv("DATABASE_URL"))

for name in ["products", "reorder_analysis", "v_abc", "v_monthly_demand", "v_turnover"]:
    pd.read_sql(f"SELECT * FROM inv.{name}", eng).to_csv(f"data/{name}.csv", index=False)
    print("exported", name)