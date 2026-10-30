CREATE OR REPLACE VIEW inv.v_turnover AS
SELECT p.sku, p.category,
       SUM(m.sales_qty * p.unit_cost)            AS cogs,
       AVG(m.on_hand * p.unit_cost)              AS avg_inventory_value,
       SUM(m.sales_qty * p.unit_cost) / NULLIF(AVG(m.on_hand * p.unit_cost),0) AS turnover,
       365 / NULLIF(SUM(m.sales_qty * p.unit_cost) / NULLIF(AVG(m.on_hand * p.unit_cost),0),0) AS days_of_inventory
FROM inv.stock_movements m JOIN inv.products p USING (sku)
WHERE m.date >= DATE '2025-10-01'
GROUP BY p.sku, p.category;