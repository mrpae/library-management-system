DROP TABLE IF EXISTS adminaccs; 

CREATE TABLE adminaccs (
    acc_id INT PRIMARY KEY,
    name VARCHAR(255),
    username VARCHAR(100),
    password VARCHAR(255),
    status CHAR(1) CHECK (status IN ('Y', 'N')),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

COPY adminaccs(acc_id, name, username, password, status, created_at, updated_at)
FROM '/tmp/data/adminaccs.csv'
DELIMITER ','
CSV HEADER;