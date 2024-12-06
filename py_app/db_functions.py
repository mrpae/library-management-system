import os 
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import string
from datetime import datetime, timedelta, date
import random
load_dotenv()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def log_in_user(username, password):
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()
        # in real world we'd do hashing of pw
        cur.execute("SELECT COUNT(*) from LUser WHERE email=%s AND pw_hash=%s", (username, password))
        count = cur.fetchone()[0]
        # returns true of false, based on if the log in was successful
        message = "logging in successful" if count == 1 else "logging in failed"
        print(message)
        return count == 1
    except:
        return 'error'
    finally:
        if conn:
            cur.close()
            conn.close()

def add_new_user(first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id):
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )        
        cur = conn.cursor()
        # in real world we'd do hashing of pw
        id = id_generator(size=10)
        cur.execute("""INSERT INTO LUser(user_id, first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (id, first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id))
        conn.commit()    
        print(f"New user added, with id '{id}'")
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def get_all_users_from_specific_user_group(user_group_id):
    '''
    1;Student
    2;Librarian
    3;Admin
    '''
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()
        cur.execute("SELECT user_id, first_name, last_name, email, postal_address, phone_nr, is_ut_student from LUser WHERE fk_user_group_id = %s", (user_group_id,))
        data = cur.fetchall()
        return pd.DataFrame.from_records(data)
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def add_new_card_for_user(user_id):
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()
        card_id = id_generator(size=15)
        cur.execute("INSERT INTO Card(card_id, exp_date, fk_user_id) VALUES(%s, %s, %s)", (card_id, date(2099, 12, 31), user_id))
        conn.commit()
        print(f"Card with id '{card_id}' created for user '{user_id}'")
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def get_book_copies_by_title(title):
    try:
        # returns all the book copies (that contain 'title' keyword) and also their availability
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()
        cur.execute("""SELECT 
        b.title AS book_title,
        bc.book_copy_id as copy_id,
        bc.barcode as barcode,
        b.book_id,
        CASE 
            WHEN l.loan_id IS NOT NULL AND l.return_date IS NULL THEN 'Reserved'
            ELSE 'Available'
        END AS status,
        l.due_date AS reserved_until
        FROM 
            Book_copy bc
        JOIN 
            Book b ON bc.fk_book_id = b.book_id
        LEFT JOIN 
            Loan l ON bc.book_copy_id = l.fk_book_copy_id AND l.return_date IS NULL
        WHERE
            b.title ILIKE %s
        ORDER BY 
            b.title, bc.book_copy_id;
        """, (f'%{title}%',))
        data = cur.fetchall()
        return pd.DataFrame.from_records(data)
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def reserve_book(book_id, user_id):
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()
        # Find the earliest due date for the book
        cur.execute(
        """
        SELECT MIN(l.due_date)
        FROM Loan l
        JOIN Book_copy bc ON l.fk_book_copy_id = bc.book_copy_id
        WHERE bc.fk_book_id = %s AND l.return_date IS NULL
        """,
        (book_id,)
        )
        earliest_due_date = cur.fetchone()[0]
    
        if earliest_due_date:
            # Calculate reservation_end as earliest_due_date + 5 days
            reservation_end = earliest_due_date + timedelta(days=5)
        else:
            # If no loans exist, set reservation_end to 5 days from today
            reservation_end = datetime.now() + timedelta(days=5)
        cur.execute("""INSERT INTO Reservation(reservation_id, reserve_date, reservation_end, fk_book_id, fk_user_id) 
                VALUES (nextval('reservation_reservation_id_seq'), %s, %s, %s, %s)""", (datetime.now(), reservation_end, book_id, user_id))
        conn.commit()
        cur.execute(
        """
        SELECT 
            b.title,
            r.reserve_date,
            r.reservation_end,
            fk_user_id as user_id
        FROM 
            Reservation r
        JOIN 
            Book b ON r.fk_book_id = b.book_id
        WHERE 
            fk_book_id = %s
        ORDER BY 
            reserve_date ASC;
        """,
        (book_id,)
        )
        data = cur.fetchall()
        return pd.DataFrame.from_records(data)
    except Exception as e:
        return e
    finally:
    # Close the connection
        if conn:
            cur.close()
            conn.close()   

def loan_book_and_get_loans(book_copy_id, card_id):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT loan_id 
            FROM Loan 
            WHERE fk_book_copy_id = %s 
            AND return_date IS NULL
        """, (book_copy_id,))

        # If there is a result, the book is already loaned out
        if cur.fetchone():
            print(f"Book copy {book_copy_id} is already loaned out.")
            return

        # Loan the book
        cur.execute(
            """
            INSERT INTO Loan (loan_id, fk_card_id, fk_book_copy_id)
            VALUES (nextval('loan_loan_id_seq'), %s, %s)
            """,
            (card_id, book_copy_id)
        )
        conn.commit()

        print(f"Book copy {book_copy_id} loaned to card ID {card_id}.")

        # Retrieve all loans ordered by newest to oldest
        cur.execute(
            """
            SELECT 
                b.title,
                l.borrow_date,
                l.due_date,
                l.return_date,
                l.fk_card_id,
                l.loan_id
            FROM 
                Loan l
            JOIN 
                Book_copy bc ON l.fk_book_copy_id = bc.book_copy_id
            JOIN 
                Book b ON bc.fk_book_id = b.book_id
            ORDER BY 
                l.borrow_date DESC, l.loan_id DESC
            """
        )
        loans = cur.fetchall()
        return pd.DataFrame.from_records(loans)
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()

def get_all_loans():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='localhost',
            port=5432
        )
        cur = conn.cursor()
        # Retrieve all loans ordered by newest to oldest
        cur.execute(
            """
            SELECT 
                b.title,
                l.borrow_date,
                l.due_date,
                l.return_date,
                l.fk_card_id,
                l.loan_id
            FROM 
                Loan l
            JOIN 
                Book_copy bc ON l.fk_book_copy_id = bc.book_copy_id
            JOIN 
                Book b ON bc.fk_book_id = b.book_id
            ORDER BY 
                l.borrow_date DESC, l.loan_id DESC
            """
        )
        loans = cur.fetchall()
        return pd.DataFrame.from_records(loans)
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()

## testing created functions

#log_in_user('jane.smith@example.com', 'hashedpassword3')
#add_new_user("Mari", "Tali", "strongPw", "mari.tali@example.com", 65631, "6426721", True, 1)
#print(get_all_users_from_specific_user_group(1))
#print(add_new_card_for_user('QYB75Z8SC2'))
#print(get_book_copies_by_title('python'))
#print(reserve_book('B002', 'QYB75Z8SC2'))
#print(get_book_copies_by_title('databases'))
#print(loan_book_and_get_loans(1, '72955OUXF6EWFNP')) # fails because that book copy is loaned out
#print(loan_book_and_get_loans(2, '72955OUXF6EWFNP')) # succeeds