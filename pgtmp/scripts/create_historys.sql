DROP TABLE IF EXISTS historys; 

CREATE TABLE historys (
    history_id INT PRIMARY KEY,
    book_id INT,
    borrower_id INT,
    date_returned TIMESTAMP,
    date_borrowed TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id)
);

COPY historys(history_id, book_id, borrower_id, date_returned, date_borrowed, created_at, updated_at)
FROM '/tmp/data/historys.csv'
DELIMITER ','
CSV HEADER;