import os 
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import string
from getpass import getpass
from datetime import datetime, timedelta, date
import random
load_dotenv()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_db_connection():
    conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host='db',
            port=5432
        )
    return conn


def log_in_user(email, plain_password):
    """
    Authenticates a user by verifying their email and password.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Use crypt() to compare the input password with the stored hash
        query = """
        SELECT COUNT(*) 
        FROM LUser 
        WHERE email = %s AND pw_hash = crypt(%s, pw_hash);
        """
        cur.execute(query, (email, plain_password))
        count = cur.fetchone()[0]
        
        if count == 1:
            print("Login successful!")
            return True
        else:
            print("Invalid credentials!")
            return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def update_password(email):
    """
    Allows a user to update their password securely.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verify the current password
        current_password = getpass("Enter your current password: ")
        query_verify = """
        SELECT COUNT(*) 
        FROM LUser 
        WHERE email = %s AND pw_hash = crypt(%s, pw_hash);
        """
        cur.execute(query_verify, (email, current_password))
        
        if cur.fetchone()[0] != 1:
            print("Current password is incorrect!")
            return
        
        # Get the new password and confirm it
        new_password = getpass("Enter your new password: ")
        confirm_new_password = getpass("Confirm your new password: ")
        
        if new_password != confirm_new_password:
            print("Passwords do not match!")
            return
        
        # Update the database with the new hashed password
        query_update = """
        UPDATE LUser 
        SET pw_hash = %s
        WHERE email = %s;
        """
        cur.execute(query_update, (new_password, email))
        
        conn.commit()
        print("Password updated successfully!")
    except Exception as e:
        print(f"Error updating password: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

def get_user_group(username):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"SELECT fk_user_group_id from LUser WHERE email='{username}'"
        cur.execute(query)
        usergroup = cur.fetchone()[0]
        return usergroup
    except:
        return 'error'
    finally:
        if conn:
            cur.close()
            conn.close()

def get_user_id(username):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"SELECT user_id from LUser WHERE email='{username}'"
        cur.execute(query)
        user_id = cur.fetchone()[0]
        return user_id
    except:
        return 'error'
    finally:
        if conn:
            cur.close()
            conn.close()


def add_new_user(first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id):
    try:
        conn = get_db_connection()      
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
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"""
            SELECT user_id, first_name, last_name, email, postal_address, phone_nr, 
                case when is_ut_student then 'Yes' else 'No' end as uni_student
            from LUser 
            WHERE fk_user_group_id = {user_group_id}
        """
        cur.execute(query)
        data = cur.fetchall()
        return pd.DataFrame.from_records(data, columns=["User ID", "First Name", "Last Name", "Email", "Postal Address", "Phone Number", "University student"])
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def add_new_card_for_user(user_id):
    try:
        conn = get_db_connection()
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
        conn = get_db_connection()
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
        copies_columns = [
            "Book Title", "Copy ID", "Barcode", "Book ID", "Status", "Reserved Until"
        ]
        return pd.DataFrame.from_records(data, columns=copies_columns)
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def reserve_book(book_id, user_id):
    try:
        conn = get_db_connection()
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
        cur.execute(f"""INSERT INTO Reservation(reserve_date, reservation_end, fk_book_id, fk_user_id) 
                VALUES ('{datetime.now()}', '{reservation_end}', '{book_id}', '{user_id}')""")
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
        conn = get_db_connection()
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
            INSERT INTO Loan (fk_card_id, fk_book_copy_id)
            VALUES (%s, %s)
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

def get_all_loans(user_id):
    try:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()
        # Retrieve all loans ordered by newest to oldest
        query = """
            SELECT 
                b.title,
                l.borrow_date,
                l.due_date,
                case when now()::date > l.due_date then 'OVERDUE' else '' end as overdue,
                l.return_date,
                l.fk_card_id,
                l.loan_id
            FROM 
                Loan l
            JOIN 
                Book_copy bc ON l.fk_book_copy_id = bc.book_copy_id
            JOIN 
                Book b ON bc.fk_book_id = b.book_id
            JOIN 
                Card c ON l.fk_card_id = c.card_id
            JOIN
                LUser lu ON c.fk_user_id = lu.user_id
            """
        if user_id != "":
            query += f"\nWHERE lu.user_id = '{user_id}'"
        query += "\nORDER BY l.borrow_date DESC, l.loan_id DESC;"
        cur.execute(query)
        loans = cur.fetchall()
        return pd.DataFrame.from_records(loans, columns=["Book Title", "Borrow Date", "Due Date", "Overdues", "Return Date", "Card ID", "Loan ID"])
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()


def receive_book_copy(loan_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Mark the loan as returned
        cur.execute(f"""
            UPDATE Loan 
            SET return_date = CURRENT_DATE 
            WHERE loan_id = {loan_id} AND return_date IS NULL;
        """)
        
        if cur.rowcount > 0:
            conn.commit()
            print(f"Loan ID {loan_id} marked as returned.")
        else:
            print(f"No active loan found with ID {loan_id}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            cur.close()
            conn.close()


def show_user_loans_and_reservations(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"""
            select reservation_id, reserve_date, reservation_end, title, nr_of_pages, year, lang_name
            from public.reservation r
            join public.book b on r.fk_book_id = b.book_id
            join public.language l on b.fk_lang_id = l.lang_id
            where r.fk_user_id = '{user_id}'
            order by reservation_id asc
            """
        )
        reservations = cur.fetchall()
        reservation_columns = [
            "Reservation ID", "Reserve Date", "Reservation End", 
            "Title", "Number of Pages", "Year", "Language"
        ]
        reservations_df = pd.DataFrame.from_records(reservations, columns=reservation_columns)
        print("All reservations:")
        if reservations_df.shape[0] > 0:
            print(reservations_df.to_string(index=False))
        else:
            print("None")
        cur.execute(
            f"""
            select loan_id, borrow_date, due_date, return_date, title, nr_of_pages, year, lang_name
            from public.loan l
            join public.book_copy bc on l.fk_book_copy_id = bc.book_copy_id
            join public.book b on bc.fk_book_id = b.book_id
            join public.language la on b.fk_lang_id = la.lang_id
            where l.fk_card_id in (
                select card_id
                from public.card c
                where fk_user_id = '{user_id}'
            )
            order by loan_id asc
            """
        )
        loans = cur.fetchall()
        loan_columns = [
            "Loan ID", "Borrow Date", "Due Date", 
            "Return Date", "Title", "Number of Pages", 
            "Year", "Language"
        ]
        loans_df = pd.DataFrame.from_records(loans, columns=loan_columns)
        print("\nAll loans:")
        if loans_df.shape[0] > 0:
            print(loans_df.to_string(index=False))
        else:
            print("None")
        return ""
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()


def list_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            select user_id, first_name || ' ' || last_name as name, email, 
                case when is_ut_student then 'Yes' else 'No' end as uni_student, group_name
            from public.luser lu
            join public.user_group ug on lu.fk_user_group_id = ug.user_group_id;
        """)
        userlist = cur.fetchall()
        userlist_columns = [
            "User ID", "Name", "Email", 
            "University student", "Access group"
        ]
        userlist_df = pd.DataFrame.from_records(userlist, columns=userlist_columns)
        print("All users:")
        if userlist_df.shape[0] > 0:
            print(userlist_df.to_string(index=False))
        else:
            print("None")
    
        return ""
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()


def list_cards():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            select card_id, status, exp_date, first_name || ' ' || last_name as cardholder_name
            from public.card c
            join public.luser lu on c.fk_user_id = lu.user_id
            order by card_id asc
        """)
        cardlist = cur.fetchall()
        cardlist_columns = [
            "Card ID", "Status", "Expiration Date", "Cardholder Name"
        ]
        cardlist_df = pd.DataFrame.from_records(cardlist, columns=cardlist_columns)
        print("All cards:")
        if cardlist_df.shape[0] > 0:
            print(cardlist_df.to_string(index=False))
        else:
            print("None")
    
        return ""
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()


def update_card(card_id, status, exp_date):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"""
            update card
            set status = '{status}', exp_date = '{exp_date}'
            where card_id = '{card_id}';
        """)
        conn.commit()
        print(f"Card with id '{card_id}' updated!")
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()


def make_query(query_rows):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = ""
        for row in query_rows:
            query += row +"\n"
        cur.execute(query)
        if query.upper().startswith("SELECT"):
            result = cur.fetchall()
            result_df = pd.DataFrame.from_records(result)
            print("All results:")
            if result_df.shape[0] > 0:
                print(result_df.to_string(index=False))
            else:
                print("None")
        else:
            conn.commit()
        return ""
    except Exception as e:
        return e
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()


def create_resource_type(resource_type_name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"""
            INSERT INTO Resource_type (name)
            VALUES ('{resource_type_name}')
            """,
            (resource_type_name)
        )
        conn.commit()

        print(f"Resource type '{resource_type_name}' added successfully!")
        cur.execute("select max(resource_type_id) from resource_type")
        resource_type_id = cur.fetchone()[0]
        return resource_type_id
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()

def add_resource(resource_name, resource_type):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"""
            INSERT INTO Resource (name, fk_resource_type_id)
            VALUES ('{resource_name}', '{resource_type}')
            """,
            (resource_name, resource_type)
        )
        conn.commit()

        print(f"Resource '{resource_name}' added successfully!")
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()


def list_resource_type():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            select resource_type_id, name
            from resource_type
            order by resource_type_id;
        """)
        resource_type_list = cur.fetchall()
        result_df = pd.DataFrame.from_records(resource_type_list, columns=["Resource type ID", "Name"])
        if result_df.shape[0] > 0:
            print(result_df.to_string(index=False))
            return ','.join(result_df["Resource type ID"].astype(str))
        else:
            print("No resource types")
            return ""
    except Exception as e:
        return e
    finally:
        if conn:
            cur.close()
            conn.close()


def view_reservations(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT 
                r.reservation_id, r.reserve_date, r.reservation_end,
                b.title AS book_title, u.first_name || ' ' || u.last_name AS reserved_by
            FROM Reservation r
            JOIN Book b ON r.fk_book_id = b.book_id
            JOIN LUser u ON r.fk_user_id = u.user_id
        """
        if user_id != "":
            query += f"\nWHERE u.user_id = '{user_id}'"
        query += "\nORDER BY r.reserve_date ASC;"
        cur.execute(query)
        reservations = cur.fetchall()
        reservation_columns = ["Reservation ID", "Reserve Date", "Reservation End", "Book Title", "Reserved By"]
        reservations_df = pd.DataFrame.from_records(reservations, columns=reservation_columns)
        
        if not reservations_df.empty:
            print(reservations_df.to_string(index=False))
        else:
            print("No active reservations.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()


def assign_resource(resource_id, card_id, start_time, end_time):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
                INSERT INTO Booking (start_time, end_time, fk_card_id, fk_resource_id)
                VALUES (%s, %s, %s, %s);
            """, (start_time, end_time, card_id, resource_id))
        
        conn.commit()
        print(f"Resource ID {resource_id} assigned successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if conn:
            cur.close()
            conn.close()


def view_bookings():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            select lu.first_name || ' ' || lu.last_name,
                booking_id,
                start_time,
                end_time,
                card_id,
                r.name,
                rt.name,
                lu.email,
                lu.phone_nr,
                case when lu.is_ut_student then 'Yes' else 'No' end as university_student
            from booking b
            join card c on b.fk_card_id = c.card_id
            join resource r on b.fk_resource_id = r.resource_id
            join resource_type rt on r.fk_resource_type_id = rt.resource_type_id
            join luser lu on c.fk_user_id = lu.user_id
        """
        cur.execute(query)
        bookings = cur.fetchall()
        bookings_columns = ["User Name", "Booking ID", "Start Time", "End Time", "Card ID",
                            "Resource Name", "Resource Type", "User Email", "User Phone", "University Student"]
        bookings_df = pd.DataFrame.from_records(bookings, columns=bookings_columns)
        
        if not bookings_df.empty:
            print(bookings_df.to_string(index=False))
        else:
            print("No bookings found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()