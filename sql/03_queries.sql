-- ============================================
-- BUSINESS QUERIES
-- ============================================

-- Q1: Equipment maintenance cost by type (last 12 months)
SELECT 
    e.equipment_tag,
    e.equipment_type,
    mt.type_name,
    COUNT(wo.work_order_id) AS work_order_count,
    SUM(wo.cost) AS total_cost,
    SUM(wo.downtime_hours) AS total_downtime_hours,
    ROUND(AVG(wo.cost), 2) AS avg_cost
FROM work_order wo
JOIN equipment e ON wo.equipment_id = e.equipment_id
JOIN maintenance_type mt ON wo.type_id = mt.type_id
WHERE wo.start_date >= DATE('now', '-12 months')
  AND wo.status = 'completed'
GROUP BY e.equipment_tag, e.equipment_type, mt.type_name
ORDER BY total_cost DESC;

-- Q2: Top 5 most expensive work orders with parts breakdown
SELECT 
    wo.work_order_id,
    e.equipment_tag,
    mt.type_name,
    wo.cost AS labor_cost,
    COALESCE(SUM(p.unit_cost * wop.quantity_used), 0) AS parts_cost,
    wo.cost + COALESCE(SUM(p.unit_cost * wop.quantity_used), 0) AS total_cost,
    wo.downtime_hours
FROM work_order wo
JOIN equipment e ON wo.equipment_id = e.equipment_id
JOIN maintenance_type mt ON wo.type_id = mt.type_id
LEFT JOIN work_order_part wop ON wo.work_order_id = wop.work_order_id
LEFT JOIN part p ON wop.part_id = p.part_id
WHERE wo.status = 'completed'
GROUP BY wo.work_order_id
ORDER BY total_cost DESC
LIMIT 5;

-- Q3: Engineer workload and utilization
SELECT 
    eng.name,
    eng.specialization,
    COUNT(DISTINCT woa.work_order_id) AS work_orders,
    SUM(woa.hours_worked) AS total_hours,
    ROUND(SUM(woa.hours_worked) * eng.hourly_rate, 2) AS total_earnings,
    ROUND(AVG(woa.hours_worked), 2) AS avg_hours_per_wo
FROM engineer eng
JOIN work_order_assignment woa ON eng.engineer_id = woa.engineer_id
JOIN work_order wo ON woa.work_order_id = wo.work_order_id
WHERE wo.status = 'completed'
GROUP BY eng.engineer_id
ORDER BY total_hours DESC;

-- Q4: Equipment reliability metrics (MTBF, MTTR)
SELECT 
    e.equipment_tag,
    e.equipment_type,
    COUNT(wo.work_order_id) AS failure_count,
    ROUND(AVG(wo.downtime_hours), 2) AS mttr_hours,
    ROUND(
        (julianday('now') - julianday(MIN(wo.start_date))) / 
        NULLIF(COUNT(wo.work_order_id), 0), 2
    ) AS mtbf_days,
    SUM(wo.cost) AS total_maintenance_cost
FROM equipment e
LEFT JOIN work_order wo ON e.equipment_id = wo.equipment_id 
    AND wo.type_id IN (2, 3)  -- corrective + predictive
    AND wo.status = 'completed'
GROUP BY e.equipment_id
ORDER BY failure_count DESC;

-- Q5: Parts inventory status with reorder alerts
SELECT 
    p.part_number,
    p.part_name,
    p.category,
    p.stock_quantity,
    p.reorder_level,
    CASE 
        WHEN p.stock_quantity <= p.reorder_level THEN 'REORDER NOW'
        WHEN p.stock_quantity <= p.reorder_level * 1.5 THEN 'REORDER SOON'
        ELSE 'OK'
    END AS stock_status,
    p.unit_cost,
    p.stock_quantity * p.unit_cost AS inventory_value
FROM part p
ORDER BY 
    CASE WHEN p.stock_quantity <= p.reorder_level THEN 0 ELSE 1 END,
    p.stock_quantity ASC;

-- Q6: Monthly maintenance cost trend
SELECT 
    strftime('%Y-%m', wo.start_date) AS month,
    COUNT(wo.work_order_id) AS work_orders,
    SUM(wo.cost) AS total_cost,
    SUM(wo.downtime_hours) AS downtime_hours,
    ROUND(SUM(wo.cost) / NULLIF(SUM(wo.downtime_hours), 0), 2) AS cost_per_downtime_hour
FROM work_order wo
WHERE wo.status = 'completed'
GROUP BY month
ORDER BY month;

-- Q7: Equipment with highest downtime in last 6 months
SELECT 
    e.equipment_tag,
    e.location,
    SUM(wo.downtime_hours) AS total_downtime,
    COUNT(wo.work_order_id) AS work_order_count,
    ROUND(SUM(wo.downtime_hours) / COUNT(wo.work_order_id), 2) AS avg_downtime_per_wo
FROM equipment e
JOIN work_order wo ON e.equipment_id = wo.equipment_id
WHERE wo.start_date >= DATE('now', '-6 months')
  AND wo.status = 'completed'
GROUP BY e.equipment_id
HAVING total_downtime > 0
ORDER BY total_downtime DESC;
