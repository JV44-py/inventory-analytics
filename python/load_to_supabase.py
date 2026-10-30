import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
eng = create_engine(os.getenv("DATABASE_URL"))

pd.read_csv("data/products.csv").to_sql(
    "products", eng, schema="inv", if_exists="replace", index=False)

pd.read_csv("data/stock_movements.csv", parse_dates=["date"]).to_sql(
    "stock_movements", eng, schema="inv", if_exists="replace",
    index=False, chunksize=5000, method="multi")

print("Loaded.")