-- ============================================
-- STORED PROCEDURES (SQLite-compatible as parameterized queries)
-- ============================================

-- Note: SQLite doesn't support stored procedures natively.
-- These are shown as PostgreSQL/MySQL syntax for reference,
-- with SQLite-compatible Python implementations.

/*
-- PostgreSQL version:
CREATE OR REPLACE FUNCTION create_work_order(
    p_equipment_id INTEGER,
    p_type_id INTEGER,
    p_start_date DATE,
    p_notes TEXT
) RETURNS INTEGER AS $$
DECLARE
    new_wo_id INTEGER;
BEGIN
    INSERT INTO work_order (equipment_id, type_id, start_date, status, notes)
    VALUES (p_equipment_id, p_type_id, p_start_date, 'planned', p_notes)
    RETURNING work_order_id INTO new_wo_id;
    
    RETURN new_wo_id;
END;
$$ LANGUAGE plpgsql;
*/

-- SQLite Python implementation:
-- See scripts/setup_db.py for equivalent functionality
