# python/generate_data.py
import numpy as np, pandas as pd
rng = np.random.default_rng(42)

N = 150
cats = ["Electronics","Home","Apparel","Grocery","Office"]
products = pd.DataFrame({
    "sku": [f"SKU{i:04d}" for i in range(N)],
    "category": rng.choice(cats, N),
    "unit_cost": rng.uniform(2, 80, N).round(2),
    "lead_time_days": rng.integers(3, 21, N),
    "base_demand": rng.gamma(2, 6, N).round(1),   # avg units/day
})
products["unit_price"] = (products.unit_cost * rng.uniform(1.2, 1.8, N)).round(2)

dates = pd.date_range("2024-10-01", "2026-09-30")
rows = []
for _, p in products.iterrows():
    on_hand = int(p.base_demand * 30)
    pipeline = {}                       # arrival_date -> qty
    rop_naive = p.base_demand * p.lead_time_days * 1.1
    for d in dates:
        season = 1 + 0.3*np.sin(2*np.pi*(d.dayofyear-80)/365)
        if p.category == "Apparel" and d.month in (11, 12): season *= 1.5
        demand = rng.poisson(max(p.base_demand * season, 0.1))
        receipt = pipeline.pop(d, 0)
        on_hand += receipt
        sold = min(demand, on_hand)
        on_hand -= sold
        if on_hand + sum(pipeline.values()) <= rop_naive:
            pipeline[d + pd.Timedelta(days=int(p.lead_time_days))] = int(p.base_demand * 30)
        rows.append((d, p.sku, demand, sold, receipt, on_hand))

movements = pd.DataFrame(rows, columns=["date","sku","demand_qty","sales_qty","receipt_qty","on_hand"])
products.to_csv("data/products.csv", index=False)
movements.to_csv("data/stock_movements.csv", index=False)