CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wing_width FLOAT,
    wing_length FLOAT,
    seq_id INT,
    time_sec FLOAT,
    heli_id INT,
    group_id VARCHAR(50)
);

