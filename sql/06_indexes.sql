-- ============================================
-- PERFORMANCE INDEXES
-- ============================================

-- Work order lookups
CREATE INDEX idx_wo_equipment ON work_order(equipment_id);
CREATE INDEX idx_wo_status ON work_order(status);
CREATE INDEX idx_wo_start_date ON work_order(start_date);
CREATE INDEX idx_wo_type ON work_order(type_id);

-- Sensor readings (time-series queries)
CREATE INDEX idx_sr_equipment_time ON sensor_reading(equipment_id, reading_time);
CREATE INDEX idx_sr_time ON sensor_reading(reading_time);

-- Equipment lookups
CREATE INDEX idx_eq_tag ON equipment(equipment_tag);
CREATE INDEX idx_eq_type ON equipment(equipment_type);
CREATE INDEX idx_eq_status ON equipment(status);

-- Parts
CREATE INDEX idx_part_number ON part(part_number);
CREATE INDEX idx_part_category ON part(category);

-- Assignments
CREATE INDEX idx_woa_engineer ON work_order_assignment(engineer_id);
CREATE INDEX idx_woa_wo ON work_order_assignment(work_order_id);
