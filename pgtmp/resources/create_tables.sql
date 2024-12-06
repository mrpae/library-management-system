DROP TABLE IF EXISTS Book_subject;
DROP TABLE IF EXISTS Loan;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Book_copy;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Language;
DROP TABLE IF EXISTS Subject;
DROP TABLE IF EXISTS Publisher;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Card;
DROP TABLE IF EXISTS Resource;
DROP TABLE IF EXISTS LUser;
DROP TABLE IF EXISTS User_group;
DROP TABLE IF EXISTS Resource_type;

CREATE TABLE Language (
    lang_id SERIAL PRIMARY KEY,
    lang_name VARCHAR(100) NOT NULL
);

CREATE TABLE Book (
    book_id VARCHAR(13) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    nr_of_pages INTEGER NOT NULL,
    year INTEGER NOT NULL,
    fk_lang_id SERIAL NOT NULL,
    FOREIGN KEY (fk_lang_id) REFERENCES Language(lang_id)
);

CREATE TABLE Subject (
    sub_id SERIAL PRIMARY KEY,
    keyword VARCHAR(200) NOT NULL,
    description TEXT
);

CREATE TABLE Book_subject (
    book_sub_id SERIAL PRIMARY KEY,
    fk_subject_id SERIAL NOT NULL,
    fk_book_id VARCHAR(13) NOT NULL,
    FOREIGN KEY (fk_subject_id) REFERENCES Subject(sub_id),
    FOREIGN KEY (fk_book_id) REFERENCES Book(book_id)
);

CREATE TABLE Publisher (
    pub_id SERIAL PRIMARY KEY,
    pub_name VARCHAR(200) NOT NULL
);

CREATE TABLE Author (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

CREATE TABLE Book_author (
    book_author_id SERIAL PRIMARY KEY,
    fk_book_id VARCHAR(13) NOT NULL,
    fk_author_id SERIAL NOT NULL,
    FOREIGN KEY (fk_book_id) REFERENCES Book(book_id),
    FOREIGN KEY (fk_author_id) REFERENCES Author(author_id)
);

CREATE TABLE User_group (
    user_group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL
);

CREATE TABLE LUser (
    user_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    pw_hash VARCHAR(500) NOT NULL,
    email VARCHAR(100) NOT NULL,
    postal_address VARCHAR(200),
    phone_nr VARCHAR(20),
    is_ut_student BOOLEAN DEFAULT FALSE NOT NULL,
     fk_user_group_id SERIAL NOT NULL,
    FOREIGN KEY (fk_user_group_id) REFERENCES User_group(user_group_id)
);

CREATE TABLE Card (
    card_id VARCHAR(15) PRIMARY KEY,
    activation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'active' NOT NULL,
    exp_date DATE,
    fk_user_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (fk_user_id) REFERENCES LUser(user_id)
);

CREATE TABLE Resource_type (
    resource_type_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE Resource (
    resource_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    fk_resource_type_id SERIAL NOT NULL,
    FOREIGN KEY (fk_resource_type_id) REFERENCES Resource_type(resource_type_id)
);

CREATE TABLE Book_copy (
    book_copy_id SERIAL PRIMARY KEY,
    barcode VARCHAR(15) NOT NULL,
    price FLOAT(2) NOT NULL,
    purchase_date DATE NOT NULL,
    fk_book_id VARCHAR(13) NOT NULL,
    FOREIGN KEY (fk_book_id) REFERENCES Book(book_id)
);

CREATE TABLE Loan (
    loan_id SERIAL PRIMARY KEY,
    borrow_date DATE DEFAULT CURRENT_DATE NOT NULL,
    due_date DATE DEFAULT (CURRENT_DATE + INTERVAL '15 DAYS') NOT NULL,
    return_date DATE,
    fk_card_id VARCHAR(15) NOT NULL,
    fk_book_copy_id SERIAL NOT NULL,
    FOREIGN KEY (fk_card_id) REFERENCES Card(card_id),
    FOREIGN KEY (fk_book_copy_id) REFERENCES Book_copy(book_copy_id)
);

CREATE TABLE Reservation (
    reservation_id SERIAL PRIMARY KEY,
    reserve_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    reservation_end DATE NOT NULL,
    fk_book_id VARCHAR(13) NOT NULL,
    fk_user_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (fk_book_id) REFERENCES Book(book_id),
    FOREIGN KEY (fk_user_id) REFERENCES LUser(user_id),
    CONSTRAINT chk_reservation_end CHECK (reservation_end >= reserve_date)
);

CREATE TABLE Booking (
    booking_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    fk_card_id VARCHAR(15) NOT NULL,
    fk_resource_id SERIAL NOT NULL,
    FOREIGN KEY (fk_card_id) REFERENCES Card(card_id),
    FOREIGN KEY (fk_resource_id) REFERENCES Resource(resource_id),
    CONSTRAINT chk_booking_end_time CHECK (end_time >= start_time)
);
