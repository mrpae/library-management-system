DROP TABLE IF EXISTS borrowers; 

CREATE TABLE borrowers (
    borrower_id INT PRIMARY KEY,
    fullname VARCHAR(50),
    gender VARCHAR(10),
    address VARCHAR(100),
    vio_count INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    resetmonth INT
);

COPY borrowers(borrower_id, fullname, gender, address, vio_count, created_at, updated_at, resetmonth)
FROM '/tmp/data/borrowers.csv'
DELIMITER ','
CSV HEADER;