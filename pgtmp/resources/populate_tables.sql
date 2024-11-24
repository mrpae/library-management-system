COPY User_group(user_group_id, group_name)
FROM '/tmp/resources/User_group.csv'
DELIMITER ';'
CSV HEADER;

COPY LUser(user_id, first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id)
FROM '/tmp/resources/User.csv'
DELIMITER ';'
CSV HEADER;

COPY Publisher(pub_id, pub_name)
FROM '/tmp/resources/Publisher.csv'
DELIMITER ';'
CSV HEADER;

COPY Subject(sub_id, keyword, description)
FROM '/tmp/resources/Subject.csv'
DELIMITER ';'
CSV HEADER;

COPY Language(lang_id, lang_name)
FROM '/tmp/resources/Language.csv'
DELIMITER ';'
CSV HEADER;

COPY Book(book_id, title, nr_of_pages, year, fk_lang_id)
FROM '/tmp/resources/Book.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_subject(book_sub_id, fk_subject_id, fk_book_id)
FROM '/tmp/resources/Book_subject.csv'
DELIMITER ';'
CSV HEADER;

COPY Author(author_id, first_name, last_name)
FROM '/tmp/resources/Author.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_author(book_author_id, fk_book_id, fk_author_id)
FROM '/tmp/resources/Book_author.csv'
DELIMITER ';'
CSV HEADER;

COPY Book_copy(book_copy_id, barcode, price, purchase_date, fk_book_id)
FROM '/tmp/resources/Book_copy.csv'
DELIMITER ';'
CSV HEADER;

COPY Card(card_id, activation_date, status, fk_user_id, exp_date)
FROM '/tmp/resources/Card.csv'
DELIMITER ';'
CSV HEADER;

COPY Loan(loan_id, borrow_date, due_date, return_date, fk_card_id, fk_book_copy_id)
FROM '/tmp/resources/Loan.csv'
DELIMITER ';'
CSV HEADER;

COPY Reservation(reservation_id, reserve_date, reservation_end, fk_book_id, fk_user_id)
FROM '/tmp/resources/Reservation.csv'
DELIMITER ';'
CSV HEADER;

COPY Resource_type(resource_type_id, name)
FROM '/tmp/resources/Resource_type.csv'
DELIMITER ';'
CSV HEADER;

COPY Resource(resource_id, name, fk_resource_type_id)
FROM '/tmp/resources/Resource.csv'
DELIMITER ';'
CSV HEADER;

COPY Booking(booking_id, start_time, end_time, fk_card_id, fk_resource_id)
FROM '/tmp/resources/Booking.csv'
DELIMITER ';'
CSV HEADER;
