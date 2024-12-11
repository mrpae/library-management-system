import getpass
import os
import pandas as pd
from datetime import datetime
from db_functions import (
    log_in_user,
    add_new_user,
    add_new_card_for_user,
    get_book_copies_by_title,
    get_all_users_from_specific_user_group,
    reserve_book,
    receive_book_copy,
    loan_book_and_get_loans,
    get_all_loans,
    get_user_group,
    get_user_id,
    update_password,
    show_user_loans_and_reservations,
    view_reservations,
    list_users,
    list_cards,
    update_card,
    make_query,
    list_resource_type,
    add_resource,
    create_resource_type,
    assign_resource,
    view_bookings
)

def admin_menu(email):
    os.system('clear')
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add new user")
        print("2. Add new card for a user")
        print("3. Activate/deactivate cards")
        print("4. Add a resource")
        print("5. Make a query")
        print("6. View all loans")
        print("7. Update your password")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            first_name = input("First name: ")
            last_name = input("Last name: ")
            email = input("Email: ")
            postal_address = input("Postal address: ")
            phone_nr = input("Phone number: ")
            is_ut_student = input("Is UT student (True/False): ").lower() == 'true'
            password = getpass.getpass("Password: ")
            fk_user_group_id = int(input("User group ID (1=Student, 2=Librarian, 3=Admin): "))
            result = add_new_user(first_name, last_name, password, email, postal_address, phone_nr, is_ut_student, fk_user_group_id)
            print(result if result else "User added successfully!")
        
        elif choice == "2":
            list_users()
            user_id = input("Enter user ID: ")
            result = add_new_card_for_user(user_id)
            print(result if result else "Card added successfully!")

        elif choice == "3":
            list_cards()
            card_id = input("Enter card ID you wish to modify: ")
            if card_id != "":
                status = input("Updated status (active/inactive): ")
                exp_date = input("Set expiration date (YYYY-MM-DD): ")
                if status != "" or exp_date != "":
                    update_card(card_id, status, exp_date)
        
        elif choice == "4":
            resource_name = input("Enter resource name: ")
            if resource_name != "":
                resource_ids = list_resource_type()
                resource_type = input("Enter resource type ID (or 'other' if you want to add a new one): ")
                if resource_type in resource_ids:
                    add_resource(resource_name, resource_type)
                elif resource_type.upper() == 'OTHER':
                    resource_type_name = input("Insert new resource type name: ")
                    new_id = create_resource_type(resource_type_name)
                    add_resource(resource_name, new_id)
                else:
                    print("Invalid resource type ID!")

        elif choice == "5":
            print("Insert query row by row. Insert an empty row to break.\n")
            query_rows = []
            while True:
                row = input("")
                if row == "":
                    break
                else:
                    query_rows.append(row)
            make_query(query_rows)
        
        elif choice == "6":
            loans = get_all_loans("")
            print(loans.to_string(index=False))

        elif choice == "7":
            email = input("Enter your email: ")
            update_password(email)
        
        elif choice == "8":
            break
        
        else:
            print("Invalid choice. Please try again.")

def librarian_menu(email):
    os.system('clear')
    while True:
        print("\n--- Librarian Menu ---")
        print("1. Search book copies by title")
        print("2. View student profiles")
        print("3. View reservations")
        print("4. View loans")
        print("5. View resource bookings")
        print("6. Loan a book copy")
        print("7. Receive a book copy")
        print("8. Assign resources")
        print("9. Update your password")
        print("10. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title keyword: ")
            books = get_book_copies_by_title(title)
            if isinstance(books, pd.DataFrame) and not books.empty:
                print(books.to_string(index=False))
            elif isinstance(books, Exception):
                print(f"An error occurred: {books}")
            else:
                print("No book copies found.")

        elif choice == "2":
            students = get_all_users_from_specific_user_group(1)  # User group ID 1 = Students
            if isinstance(students, pd.DataFrame) and not students.empty:
                print(students.to_string(index=False))
            elif isinstance(students, Exception):
                print(f"An error occurred: {students}")
            else:
                print("No student profiles found.")

        elif choice == "3":
            user_id = input("Insert user ID or leave empty if you wish to see all reservations: ")
            view_reservations(user_id)

        elif choice == "4":
            user_id = input("Insert user ID or leave empty if you wish to see all loans: ")
            loans = get_all_loans(user_id)
            if isinstance(loans, pd.DataFrame) and not loans.empty:
                print(loans.to_string(index=False))
            elif isinstance(loans, Exception):
                print(f"An error occurred: {loans}")
            else:
                print("No loans found.")

        elif choice == "5":
            print("All bookings: ")
            view_bookings("")
        
        elif choice == "6":
            try:
                book_copy_id = int(input("Enter book copy ID to loan: "))
                card_id = input("Enter card ID: ")
                result = loan_book_and_get_loans(book_copy_id, card_id)
                if isinstance(result, pd.DataFrame) and not result.empty:
                    print(result.to_string(index=False))
                    print("Book loaned successfully!")
                elif isinstance(result, Exception):
                    print(f"An error occurred: {result}")
                else:
                    print("Loan operation failed.")
            except ValueError:
                print("Invalid input. Please enter valid IDs.")

        elif choice == "7":
            loan_id = input("Enter loan ID to mark as returned: ")
            receive_book_copy(loan_id)

        elif choice == "8":
            resource_id = input("Enter resource ID to assign: ")
            card_id = input("Enter card ID of the user: ")
            
            # Assign resource by creating a booking
            start_time = datetime.now()
            end_time_str = input("Enter end time (YYYY-MM-DD HH:MM): ")
            try:
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
                assign_resource(resource_id, card_id, start_time, end_time)
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD HH:MM")

        elif choice == "9":
            update_password(email)
        
        elif choice == "10":
            break
        
        else:
            print("Invalid choice. Please try again.")

def student_menu(user_id, email):
    os.system('clear')
    while True:
        print("\n--- Student Menu ---")
        print("1. Search available books by title")
        print("2. Reserve a book")
        print("3. Show all my loans and reservations")
        print("4. Update your password")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title keyword: ")
            books = get_book_copies_by_title(title)
            if isinstance(books, pd.DataFrame) and not books.empty:
                print(books.to_string(index=False))
            elif isinstance(books, Exception):
                print(f"An error occurred: {books}")
            else:
                print("No book copies found.")
        
        elif choice == "2":
            book_id = input("Enter book ID to reserve: ")
            result = reserve_book(book_id, user_id)
            if isinstance(result, Exception):
                print(f"An error occurred: {result}")
            else:
                print("Book reserved successfully!")

        elif choice == "3":
            show_results = show_user_loans_and_reservations(user_id)
            if isinstance(show_results, Exception):
                print(f"An error occurred: {show_results}")
            print("\nAll bookings: ")
            view_bookings(user_id)

        elif choice == "4":
            update_password(email)
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("--- Library Management System ---")
        email = input("Enter email: ")
        password = getpass.getpass("Enter password: ")

        # Log in the user
        if log_in_user(email, password):
            user_id = get_user_id(email)
            user_group_id = get_user_group(email)
            
            if user_group_id == 1:
                student_menu(user_id, email)
            elif user_group_id == 2:
                librarian_menu(email)
            elif user_group_id == 3:
                admin_menu(email)
            else:
                print("Invalid role selected.")
            os.system('clear')
        else:
            print("\nLogin failed. Please check your credentials.")
            retry = input("Do you want to retry? (y/n): ").strip().lower()
            if retry == 'y':
                os.system('clear')
            else:
                print("Exiting the system. Goodbye!")
                break

if __name__ == "__main__":
    main()