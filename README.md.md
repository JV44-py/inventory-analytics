# Supply Chain & Inventory Analytics

An end-to-end operations analytics project that answers four questions about a product inventory: how fast does stock turn over, how does stock move, what are the demand trends, and when should each SKU be reordered?

> **Note:** The dataset is simulated (generated with Python) so the full pipeline could be built and explained end to end. No real company data is used.

## Tech stack
- **PostgreSQL** (Supabase) for storage and SQL views
- **Python** (pandas, NumPy, SQLAlchemy) for data generation, loading, and reorder-point analysis
- **Power BI Desktop** for the 3-page dashboard
- **Git / GitHub** for version control

## Pipeline
```
generate_data.py  ->  CSV files  ->  load_to_supabase.py  ->  Postgres schema "inv"
                                                                   |
                                         SQL views (turnover, monthly demand, ABC)
                                                                   |
                                reorder_analysis.py  ->  inv.reorder_analysis
                                                                   |
                                  export_for_powerbi.py  ->  CSVs  ->  Power BI dashboard
```

## Dataset (simulated)
- 150 SKUs across 5 categories (Electronics, Home, Apparel, Grocery, Office)
- 730 days of history (Oct 2024 to Sep 2026), 109,500 daily records
- Poisson-distributed daily demand with seasonality, supplier lead times of 3 to 20 days, and a baseline reorder rule that triggers at 1.1 x lead-time demand
- Tables: `inv.products` and `inv.stock_movements` (demand, units sold, receipts, on-hand stock per SKU per day)

## Methods
- **Inventory turnover** = COGS / average inventory value (last 12 months); **days of inventory** = 365 / turnover
- **ABC classification:** A = SKUs making up the first 80% of cumulative revenue, B = next 15%, C = last 5%
- **Reorder point** = (average daily demand x lead time) + safety stock
- **Safety stock** = Z x standard deviation of daily demand x sqrt(lead time), with Z = 1.65 (95% service level)
- **Status flags:** below reorder point when on-hand <= reorder point; overstock when on-hand > 3 x reorder point

## Key findings
- **Turnover:** about 22x per year, or roughly 16 days of inventory on hand, with an average inventory value of about 1.26M.
- **Seasonality:** demand rises through the spring and summer months and falls around the start of each year.
- **Stockouts are mild and spread out:** 1.83% of demand went unfilled over two years. Grocery and Apparel have the most lost units and Electronics the fewest. The worst single SKU lost 649 units, so no one product dominates the problem.
- **Reorder points:** 82 of 150 SKUs are currently below their calculated reorder point, 48 are OK, and 20 are overstocked (about 245.9K in inventory value, in simulated currency units).
- **Baseline policy gap:** the baseline trigger (1.1 x lead-time demand, no safety stock) was lower than the statistically derived reorder point for 149 of 150 SKUs.
- **ABC classes:** 64 SKUs (43%) are class A, 41 (27%) class B, and 45 (30%) class C. Revenue is less concentrated than in typical real-world catalogs because the simulated demand is fairly even.

## Dashboard (Power BI)
1. **Executive Overview:** KPI cards (inventory turnover, days of inventory, stockout rate, average inventory value), a category slicer, turnover by category, and the monthly demand trend.
2. **Inventory Turnover:** slowest-moving SKUs by days of inventory (with conditional formatting) and an ABC class donut chart.
3. **Demand & Stock Movement:** demand vs units sold by month, lost units by category, and the top 10 SKUs by lost units.

Screenshots are in the `docs/` folder:

![Executive Overview](docs/page1_executive_overview.png)
![Inventory Turnover](docs/page2_inventory_turnover.png)
![Demand and Stock Movement](docs/page3_demand_stock_movement.png)

## Limitations
- The data is simulated, so the findings describe the simulation and not a real business.
- The reorder status compares on-hand stock to the reorder point. A production version would use inventory position (on-hand plus units already on order), which needs open purchase-order data.
- Demand is treated as roughly normal for the safety stock formula, and a single warehouse and a single 95% service level are assumed.
- Receipts vs sales by month is not shown on the dashboard.

## Repository structure
```
inventory-analytics/
|-- data/         generated CSV files
|-- python/       generate_data.py, load_to_supabase.py, reorder_analysis.py,
|                 export_for_powerbi.py, findings.py
|-- sql/          01_v_turnover.sql, 02_v_monthly_demand.sql, 03_v_abc.sql
|-- dashboard/    inventory_dashboard.pbix
|-- docs/         dashboard screenshots
```

## How to run
1. Create a Supabase (Postgres) project and a schema: `CREATE SCHEMA IF NOT EXISTS inv;`
2. Create a virtual environment and install: `pandas numpy sqlalchemy "psycopg[binary]" python-dotenv`
3. Create a `.env` file in the project root with `DATABASE_URL=<your Postgres connection string>`
4. Run `python python/generate_data.py`, then `python python/load_to_supabase.py`
5. Run the three SQL files in `sql/` in the Supabase SQL Editor
6. Run `python python/reorder_analysis.py`, then `python python/export_for_powerbi.py`
7. Open `dashboard/inventory_dashboard.pbix` in Power BI Desktop and point the CSV sources at your local `data/` folder
