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

There are three different user groups. Sign in with either one:

* Student profile: email `bob.brown@example.com` and password `hashedpassword2`
  * Search available books by title. Try using a keyword `intro`.
  * Reserve a book by entering a book ID. For example, `B001`.
  * See all your reservations, bookings and loans. There is no need to specify anything.
  * Update your password.
  * Exit.
* Librarian profile: email `jane.smith@example.com` and password `hashedpassword3`
  * Search available books by title. Try using a keyword `intro`.
  * View the profiles of all students.
  * View reservations. Here you must enter a `user_ID` if you wish to see reservations made by a specific user or you can insert an empty string to see all reservations.
  * View loans. The logic is the same as with seeing the reservations. There is a separate column to see overdue loans.
  * View bookings. This is purely about resources other than books.
  * Loan a book copy to a student. Here you must specify `Book copy ID` and `Card ID.` Transaction fails if the copy is already loaned out.
  * Receive a book copy. Here you must specify the `Loan ID` of an active loan and it ends an active loan.
  * Assign resources. Specify `Resource ID`, `Card ID` and the end time of the booking. This adds a new row to the `Booking` table.
  * Update your password.
  * Exit.
* Admin profile: email `john.doe@example.com` and password `hashedpassword4`
  * Add a new user. This asks all necessary fields to add a new user.
  * Assign a new card for a user. This shows a list of all users and asks for a `User ID` you wish to assign a new card.
  * Activate or deactivate a card and set its expiration date. This shows a list of all cards and asks for a `Card ID` you wish to modify. Then you must specify the status and an expiration date.
  * Add a resource. This asks for a resource name and type. If the type does not exist then there is a possibility to add a new one.
  * Make a query. Any valid query works (select, update, create, delete, insert, etc.).
  * See the details of all loans.
  * Update your password.
  * Exit.
