CREATE OR REPLACE VIEW inv.v_monthly_demand AS
SELECT DATE_TRUNC('month', date) AS month, sku,
       SUM(demand_qty) AS demand, SUM(sales_qty) AS sold,
       SUM(demand_qty - sales_qty) AS lost_units
FROM inv.stock_movements GROUP BY 1, 2;