DROP TABLE IF EXISTS books; 

CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(50),
    copyright VARCHAR(50),
    no_pages INT,
    stock INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

COPY books(book_id, title, author, copyright, no_pages, stock, created_at, updated_at)
FROM '/tmp/data/books.csv'
DELIMITER ','
CSV HEADER;