-- ============================================
-- ADVANCED ANALYTICS
-- ============================================

-- A1: Equipment cost ranking with percentile
SELECT 
    equipment_tag,
    equipment_type,
    total_cost,
    ROUND(
        100.0 * (
            SELECT COUNT(*) FROM (
                SELECT SUM(cost) AS total_cost 
                FROM work_order 
                WHERE status = 'completed' 
                GROUP BY equipment_id
            ) sub WHERE sub.total_cost <= agg.total_cost
        ) / (SELECT COUNT(DISTINCT equipment_id) FROM work_order WHERE status = 'completed'),
        2
    ) AS cost_percentile
FROM (
    SELECT e.equipment_tag, e.equipment_type, SUM(wo.cost) AS total_cost
    FROM equipment e
    JOIN work_order wo ON e.equipment_id = wo.equipment_id
    WHERE wo.status = 'completed'
    GROUP BY e.equipment_id
) agg
ORDER BY total_cost DESC;

-- A2: Maintenance type distribution by equipment type
SELECT 
    e.equipment_type,
    mt.type_name,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY e.equipment_type), 2) AS pct_of_type
FROM work_order wo
JOIN equipment e ON wo.equipment_id = e.equipment_id
JOIN maintenance_type mt ON wo.type_id = mt.type_id
WHERE wo.status = 'completed'
GROUP BY e.equipment_type, mt.type_name
ORDER BY e.equipment_type, count DESC;

-- A3: Engineer specialization vs work order type efficiency
SELECT 
    eng.specialization,
    mt.type_name,
    COUNT(*) AS assignments,
    ROUND(AVG(woa.hours_worked), 2) AS avg_hours,
    ROUND(AVG(wo.downtime_hours), 2) AS avg_downtime,
    ROUND(AVG(wo.downtime_hours) / NULLIF(AVG(woa.hours_worked), 0), 2) AS efficiency_ratio
FROM work_order_assignment woa
JOIN engineer eng ON woa.engineer_id = eng.engineer_id
JOIN work_order wo ON woa.work_order_id = wo.work_order_id
JOIN maintenance_type mt ON wo.type_id = mt.type_id
WHERE wo.status = 'completed'
GROUP BY eng.specialization, mt.type_name
ORDER BY eng.specialization, efficiency_ratio DESC;

-- A4: Parts consumption analysis
SELECT 
    p.part_name,
    p.category,
    SUM(wop.quantity_used) AS total_consumed,
    SUM(wop.quantity_used * p.unit_cost) AS total_spend,
    COUNT(DISTINCT wop.work_order_id) AS used_in_work_orders,
    ROUND(AVG(wop.quantity_used), 2) AS avg_per_use
FROM part p
JOIN work_order_part wop ON p.part_id = wop.part_id
GROUP BY p.part_id
ORDER BY total_spend DESC;
