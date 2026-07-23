-- ============================================
-- REPORTING VIEWS
-- ============================================

-- V1: Comprehensive work order summary
CREATE VIEW v_work_order_summary AS
SELECT 
    wo.work_order_id,
    e.equipment_tag,
    e.equipment_type,
    e.location,
    mt.type_name AS maintenance_type,
    wo.start_date,
    wo.end_date,
    wo.status,
    wo.cost AS labor_cost,
    COALESCE(parts.parts_cost, 0) AS parts_cost,
    wo.cost + COALESCE(parts.parts_cost, 0) AS total_cost,
    wo.downtime_hours,
    wo.notes,
    GROUP_CONCAT(eng.name, ', ') AS assigned_engineers
FROM work_order wo
JOIN equipment e ON wo.equipment_id = e.equipment_id
JOIN maintenance_type mt ON wo.type_id = mt.type_id
LEFT JOIN (
    SELECT work_order_id, SUM(p.unit_cost * wop.quantity_used) AS parts_cost
    FROM work_order_part wop
    JOIN part p ON wop.part_id = p.part_id
    GROUP BY work_order_id
) parts ON wo.work_order_id = parts.work_order_id
LEFT JOIN work_order_assignment woa ON wo.work_order_id = woa.work_order_id
LEFT JOIN engineer eng ON woa.engineer_id = eng.engineer_id
GROUP BY wo.work_order_id;

-- V2: Equipment health dashboard
CREATE VIEW v_equipment_health AS
SELECT 
    e.equipment_id,
    e.equipment_tag,
    e.equipment_type,
    e.location,
    e.status,
    COALESCE(last_sr.reading_time, 'Never') AS last_reading,
    last_sr.temperature AS current_temp,
    last_sr.vibration AS current_vibration,
    COALESCE(wo_stats.total_work_orders, 0) AS total_work_orders,
    COALESCE(wo_stats.total_cost, 0) AS total_maintenance_cost,
    COALESCE(wo_stats.total_downtime, 0) AS total_downtime_hours
FROM equipment e
LEFT JOIN (
    SELECT equipment_id, reading_time, temperature, vibration,
           ROW_NUMBER() OVER (PARTITION BY equipment_id ORDER BY reading_time DESC) AS rn
    FROM sensor_reading
) last_sr ON e.equipment_id = last_sr.equipment_id AND last_sr.rn = 1
LEFT JOIN (
    SELECT equipment_id, 
           COUNT(*) AS total_work_orders,
           SUM(cost) AS total_cost,
           SUM(downtime_hours) AS total_downtime
    FROM work_order
    WHERE status = 'completed'
    GROUP BY equipment_id
) wo_stats ON e.equipment_id = wo_stats.equipment_id;

-- V3: Monthly KPI summary
CREATE VIEW v_monthly_kpi AS
SELECT 
    strftime('%Y-%m', wo.start_date) AS month,
    COUNT(wo.work_order_id) AS total_work_orders,
    SUM(CASE WHEN mt.type_name = 'preventive' THEN 1 ELSE 0 END) AS preventive_count,
    SUM(CASE WHEN mt.type_name = 'corrective' THEN 1 ELSE 0 END) AS corrective_count,
    SUM(wo.cost) AS total_cost,
    SUM(wo.downtime_hours) AS total_downtime,
    ROUND(AVG(wo.downtime_hours), 2) AS avg_downtime_per_wo,
    ROUND(
        100.0 * SUM(CASE WHEN mt.type_name = 'preventive' THEN 1 ELSE 0 END) / 
        COUNT(wo.work_order_id), 2
    ) AS preventive_percentage
FROM work_order wo
JOIN maintenance_type mt ON wo.type_id = mt.type_id
WHERE wo.status = 'completed'
GROUP BY month
ORDER BY month;
