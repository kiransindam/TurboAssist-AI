-- ============================================
-- SEED DATA
-- ============================================

-- Maintenance types
INSERT INTO maintenance_type VALUES 
(1, 'preventive', 'Scheduled preventive maintenance', 8),
(2, 'corrective', 'Unplanned corrective repair', 16),
(3, 'predictive', 'Condition-based maintenance', 6),
(4, 'overhaul', 'Major overhaul', 120),
(5, 'inspection', 'Routine inspection', 4);

-- Equipment
INSERT INTO equipment VALUES
(1, 'GT-SGT800-001', 'gas_turbine', 'SGT-800', 'Siemens Energy', '2018-03-15', 'Plant A', 'active', 57000),
(2, 'GT-SGT-800-002', 'gas_turbine', 'SGT-800', 'Siemens Energy', '2019-06-20', 'Plant A', 'active', 57000),
(3, 'ST-SST900-001', 'steam_turbine', 'SST-900', 'Siemens Energy', '2017-11-10', 'Plant B', 'active', 120000),
(4, 'CP-ZR-001', 'compressor', 'ZR-160', 'Atlas Copco', '2020-01-05', 'Plant A', 'active', 250),
(5, 'PM-CPP-001', 'pump', 'CPP-500', 'Sulzer', '2019-08-22', 'Plant B', 'maintenance', 150),
(6, 'GT-SGT-A65-001', 'gas_turbine', 'SGT-A65', 'Siemens Energy', '2016-04-18', 'Plant C', 'active', 67000),
(7, 'ST-SST-600-001', 'steam_turbine', 'SST-600', 'Siemens Energy', '2015-09-30', 'Plant C', 'active', 80000),
(8, 'CP-GR-001', 'compressor', 'GR-200', 'GE', '2021-02-14', 'Plant B', 'active', 400);

-- Engineers
INSERT INTO engineer VALUES
(1, 'Rajesh Kumar', 'mechanical', '2015-05-10', 85.0),
(2, 'Priya Sharma', 'electrical', '2017-08-22', 90.0),
(3, 'Amit Patel', 'rotating_equipment', '2014-03-15', 110.0),
(4, 'Sneha Reddy', 'instrumentation', '2019-01-08', 80.0),
(5, 'Vikram Singh', 'mechanical', '2016-11-20', 88.0);

-- Parts
INSERT INTO part VALUES
(1, 'BRG-742-001', 'Main Bearing', 'bearing', 2500.00, 25, 5),
(2, 'SEL-331-002', 'Shaft Seal', 'seal', 850.00, 40, 10),
(3, 'FLT-220-003', 'Oil Filter', 'filter', 120.00, 150, 30),
(4, 'BLD-550-004', 'Turbine Blade', 'blade', 4500.00, 12, 3),
(5, 'SNS-110-005', 'Vibration Sensor', 'sensor', 680.00, 30, 8),
(6, 'OIL-ISO46', 'Turbine Oil ISO46 (L)', 'lubricant', 15.50, 2000, 500);

-- Work orders (last 2 years)
INSERT INTO work_order VALUES
(1001, 1, 1, '2024-01-15', '2024-01-15', 'completed', 12500.00, 8, 'Routine PM'),
(1002, 1, 5, '2024-03-20', '2024-03-20', 'completed', 3200.00, 4, 'Quarterly inspection'),
(1003, 2, 2, '2024-02-10', '2024-02-12', 'completed', 28500.00, 36, 'Bearing replacement'),
(1004, 3, 1, '2024-01-22', '2024-01-23', 'completed', 18000.00, 16, 'Annual PM'),
(1005, 3, 4, '2024-06-01', '2024-06-10', 'completed', 185000.00, 240, 'Major overhaul'),
(1006, 4, 1, '2024-02-28', '2024-02-28', 'completed', 4500.00, 6, 'Compressor PM'),
(1007, 5, 2, '2024-07-05', NULL, 'in_progress', 15000.00, 0, 'Seal leak repair'),
(1008, 6, 3, '2024-04-15', '2024-04-15', 'completed', 9800.00, 8, 'Vibration analysis'),
(1009, 7, 1, '2024-03-10', '2024-03-11', 'completed', 22000.00, 20, 'Steam turbine PM'),
(1010, 8, 5, '2024-05-20', '2024-05-20', 'completed', 2800.00, 3, 'Routine inspection'),
(1011, 1, 3, '2024-08-01', '2024-08-01', 'completed', 7500.00, 5, 'Predictive maintenance'),
(1012, 2, 1, '2024-07-15', '2024-07-15', 'completed', 13000.00, 8, 'Scheduled PM'),
(1013, 6, 2, '2024-09-01', NULL, 'planned', 0, 0, 'Pending bearing check'),
(1014, 3, 5, '2024-10-01', NULL, 'planned', 0, 0, 'Annual inspection'),
(1015, 4, 1, '2024-08-20', '2024-08-20', 'completed', 4800.00, 6, 'Quarterly PM');

-- Work order parts
INSERT INTO work_order_part VALUES
(1001, 3, 4), (1001, 6, 100),
(1003, 1, 2), (1003, 2, 2), (1003, 6, 200),
(1004, 3, 6), (1004, 6, 150),
(1005, 4, 4), (1005, 1, 4), (1005, 2, 4), (1005, 6, 500),
(1006, 3, 3), (1006, 6, 80),
(1007, 2, 3),
(1008, 5, 2),
(1009, 3, 8), (1009, 6, 200),
(1011, 5, 1), (1011, 3, 2),
(1012, 3, 4), (1012, 6, 120),
(1015, 3, 3), (1015, 6, 90);

-- Work order assignments
INSERT INTO work_order_assignment VALUES
(1001, 1, 6), (1001, 3, 2),
(1003, 3, 28), (1003, 1, 8),
(1004, 1, 10), (1004, 5, 6),
(1005, 3, 80), (1005, 1, 40), (1005, 5, 40),
(1006, 5, 5),
(1007, 1, 12), (1007, 3, 8),
(1008, 4, 4), (1008, 3, 4),
(1009, 1, 14), (1009, 2, 6),
(1010, 4, 3),
(1011, 3, 5), (1011, 4, 3),
(1012, 1, 6), (1012, 5, 2),
(1015, 5, 5);

-- Sensor readings (sample)
INSERT INTO sensor_reading VALUES
(1, 1, '2024-10-01 08:00:00', 550, 1850, 2.8, 9800, 58),
(2, 1, '2024-10-01 09:00:00', 555, 1845, 2.9, 9790, 57.5),
(3, 1, '2024-10-01 10:00:00', 560, 1840, 3.0, 9780, 57),
(4, 2, '2024-10-01 08:00:00', 545, 1860, 2.5, 9850, 59),
(5, 2, '2024-10-01 09:00:00', 548, 1855, 2.6, 9840, 58.5),
(6, 3, '2024-10-01 08:00:00', 480, 2200, 1.8, 3000, 62),
(7, 3, '2024-10-01 09:00:00', 485, 2195, 1.9, 2995, 61.5),
(8, 4, '2024-10-01 08:00:00', 95, 145, 1.2, 14500, 45),
(9, 5, '2024-10-01 08:00:00', 75, 120, 2.1, 2900, 52),
(10, 6, '2024-10-01 08:00:00', 580, 1800, 3.5, 9700, 55);
