CREATE OR REPLACE VIEW inv.v_abc AS
WITH rev AS (
  SELECT p.sku, SUM(m.sales_qty * p.unit_price) AS revenue
  FROM inv.stock_movements m JOIN inv.products p USING (sku) GROUP BY p.sku),
cum AS (
  SELECT sku, revenue,
         SUM(revenue) OVER (ORDER BY revenue DESC) / SUM(revenue) OVER () AS cum_pct
  FROM rev)
SELECT *, CASE WHEN cum_pct <= 0.80 THEN 'A' WHEN cum_pct <= 0.95 THEN 'B' ELSE 'C' END AS abc_class
FROM cum;