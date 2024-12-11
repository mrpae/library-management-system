COPY User_group(group_name)
FROM '/tmp/data/User_group.csv'
DELIMITER ';'
CSV HEADER;

COPY LUser(user_id, first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id)
FROM '/tmp/data/User.csv'
DELIMITER ';'
CSV HEADER;

COPY Publisher(pub_name)
FROM '/tmp/data/Publisher.csv'
DELIMITER ';'
CSV HEADER;

COPY Subject(keyword, description)
FROM '/tmp/data/Subject.csv'
DELIMITER ';'
CSV HEADER;

COPY Language(lang_name)
FROM '/tmp/data/Language.csv'
DELIMITER ';'
CSV HEADER;

COPY Book(book_id, title, nr_of_pages, year, fk_lang_id)
FROM '/tmp/data/Book.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_publisher(fk_book_id, fk_publisher_id)
FROM '/tmp/data/Book_publisher.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_subject(fk_subject_id, fk_book_id)
FROM '/tmp/data/Book_subject.csv'
DELIMITER ';'
CSV HEADER;

COPY Author(first_name, last_name)
FROM '/tmp/data/Author.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_author(fk_book_id, fk_author_id)
FROM '/tmp/data/Book_author.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_copy(barcode, rack_nr, price, purchase_date, fk_book_id)
FROM '/tmp/data/Book_copy.csv'
DELIMITER ';'
CSV HEADER;

COPY Card(card_id, activation_date, status, fk_user_id, exp_date)
FROM '/tmp/data/Card.csv'
DELIMITER ';'
CSV HEADER;

COPY Loan(borrow_date, due_date, return_date, fk_card_id, fk_book_copy_id)
FROM '/tmp/data/Loan.csv'
DELIMITER ';'
CSV HEADER;

COPY Reservation(reserve_date, reservation_end, fk_book_id, fk_user_id)
FROM '/tmp/data/Reservation.csv'
DELIMITER ';'
CSV HEADER;

COPY Resource_type(name)
FROM '/tmp/data/Resource_type.csv'
DELIMITER ';'
CSV HEADER;

COPY Resource(name, fk_resource_type_id)
FROM '/tmp/data/Resource.csv'
DELIMITER ';'
CSV HEADER;

COPY Booking(start_time, end_time, fk_card_id, fk_resource_id)
FROM '/tmp/data/Booking.csv'
DELIMITER ';'
CSV HEADER;
