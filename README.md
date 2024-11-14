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
