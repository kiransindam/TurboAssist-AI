-- ============================================
-- TURBOMACHINERY MAINTENANCE DATABASE SCHEMA
-- ============================================

-- 1. Equipment master table
CREATE TABLE equipment (
    equipment_id    INTEGER PRIMARY KEY,
    equipment_tag   TEXT NOT NULL UNIQUE,
    equipment_type  TEXT NOT NULL CHECK (equipment_type IN ('gas_turbine', 'steam_turbine', 'compressor', 'pump')),
    model           TEXT NOT NULL,
    manufacturer    TEXT NOT NULL,
    install_date    DATE NOT NULL,
    location        TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'maintenance', 'decommissioned')),
    capacity_kw     REAL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Maintenance types
CREATE TABLE maintenance_type (
    type_id     INTEGER PRIMARY KEY,
    type_name   TEXT NOT NULL UNIQUE,
    description TEXT,
    typical_duration_hours INTEGER
);

-- 3. Maintenance work orders
CREATE TABLE work_order (
    work_order_id   INTEGER PRIMARY KEY,
    equipment_id    INTEGER NOT NULL REFERENCES equipment(equipment_id),
    type_id         INTEGER NOT NULL REFERENCES maintenance_type(type_id),
    start_date      DATE NOT NULL,
    end_date        DATE,
    status          TEXT NOT NULL DEFAULT 'planned' 
                    CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    cost            REAL DEFAULT 0,
    downtime_hours  REAL DEFAULT 0,
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Sensor readings (time-series)
CREATE TABLE sensor_reading (
    reading_id      INTEGER PRIMARY KEY,
    equipment_id    INTEGER NOT NULL REFERENCES equipment(equipment_id),
    reading_time    TIMESTAMP NOT NULL,
    temperature     REAL,
    pressure        REAL,
    vibration       REAL,
    rpm             REAL,
    oil_pressure    REAL
);

-- 5. Parts inventory
CREATE TABLE part (
    part_id         INTEGER PRIMARY KEY,
    part_number     TEXT NOT NULL UNIQUE,
    part_name       TEXT NOT NULL,
    category        TEXT NOT NULL,
    unit_cost       REAL NOT NULL,
    stock_quantity  INTEGER NOT NULL DEFAULT 0,
    reorder_level   INTEGER NOT NULL DEFAULT 10
);

-- 6. Parts used in work orders
CREATE TABLE work_order_part (
    work_order_id   INTEGER REFERENCES work_order(work_order_id),
    part_id         INTEGER REFERENCES part(part_id),
    quantity_used   INTEGER NOT NULL,
    PRIMARY KEY (work_order_id, part_id)
);

-- 7. Engineers / technicians
CREATE TABLE engineer (
    engineer_id     INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    specialization  TEXT NOT NULL,
    hire_date       DATE NOT NULL,
    hourly_rate     REAL NOT NULL
);

-- 8. Work order assignments
CREATE TABLE work_order_assignment (
    work_order_id   INTEGER REFERENCES work_order(work_order_id),
    engineer_id     INTEGER REFERENCES engineer(engineer_id),
    hours_worked    REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (work_order_id, engineer_id)
);
