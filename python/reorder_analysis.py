import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
eng = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_sql("""
    SELECT m.sku, m.date, m.demand_qty, m.on_hand, p.lead_time_days
    FROM inv.stock_movements m JOIN inv.products p USING (sku)
""", eng)

Z = 1.65  # 95% service level

stats = df.groupby("sku").agg(
    avg_demand=("demand_qty", "mean"),
    std_demand=("demand_qty", "std"),
    lead_time=("lead_time_days", "first"),
).reset_index()

stats["safety_stock"] = Z * stats.std_demand * np.sqrt(stats.lead_time)
stats["reorder_point"] = stats.avg_demand * stats.lead_time + stats.safety_stock

latest = df[df.date == df.date.max()][["sku", "on_hand"]]
out = stats.merge(latest, on="sku")

out["status"] = np.where(out.on_hand <= out.reorder_point, "BELOW REORDER POINT",
                np.where(out.on_hand > out.reorder_point * 3, "OVERSTOCK", "OK"))

out = out.round(2)
out.to_sql("reorder_analysis", eng, schema="inv", if_exists="replace", index=False)
print(out.status.value_counts())