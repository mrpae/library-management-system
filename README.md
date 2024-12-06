# Library management system

UT Databases (LTAT.02.021) project



## Walkthrough

Make sure you have installed Docker Desktop and have it running.

Run `docker compose up -d` to start the service. It should take about one minute, not longer. Once the network shows the status `Created` and the other three containers have `Started` then you should have everything up and running.

### Using PgAdmin

Go to [PgAdmin](http://localhost:5050/) and log in with the PGADMIN_DEFAULT credentials that you have defined in the `.env` file.

* `Add new server`
* Give a name as you would like
* Under `connection` tab, Host is the container name (`db`), Username and Password are in `.env`.


### DEMO
functions are in pure python file db_functions.py, if you want to test them out from commandline you might need to create virtual env (vsc suggests and does it for you) and install requirements from requirement.txt:
> /path/to/virtualEnv/library-management-system-main/.venv/bin/python -m pip install -r requirements.txt -v
Then later can run similarly: 
> /path/to/virtualEnv/library-management-system-main/.venv/bin/python db_functions.py

Lets assume we have a senario where a new Tartu uni student wants to get the library access and loan out some books.

* Start front application and log in with library credentials: email and pw (jane.smith@example.com, hashedpassword3) function (log_in_user(username, password))
* Add new student user (add_new_user(first_name, last_name, pw_hash, email, postal_address, phone_nr, is_ut_student, fk_user_group_id), after get all student users get_all_users_from_specific_user_group(user_group_id))
* Create card for student user (add_new_card_for_user(user_id))
* Search for book by title (get_book_copies_by_title(title))
* See that the book is already loaned out (only one copy exists)
* Reserve book (reserve_book(book_id, user_id))
* Loan out different kind of book (get_book_copies_by_title(title) -> loan_book_and_get_loans(book_copy_id, card_id))