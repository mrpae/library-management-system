DROP TABLE IF EXISTS transactions; 

CREATE TABLE transactions (
    transac_id INT PRIMARY KEY,
    book_id INT,
    borrower_id INT,
    dateborrowed TIMESTAMP,
    duedatereturned TIMESTAMP,
    fullname VARCHAR(100),
    booktitle VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id)
);

COPY transactions(transac_id, book_id, borrower_id, dateborrowed, duedatereturned, fullname, booktitle, created_at, updated_at)
FROM '/tmp/data/transactions.csv'
DELIMITER ','
CSV HEADER;