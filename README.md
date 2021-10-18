# csv_postgres_connector

Goals:

1. Connect to Postgres using psycopg2
2. Import csv's into a Postgres DB

Start Date: 10/12

🐢 10/12

Replaced pd datatypes with sql datatypes and connected to DB.

🐢 10/13

MVP complete. Uploaded entire csv file. Closed cursor.

🐢 10/14

Started automation. Rename csv names to lower case and get rid of symbols.

🐢 10/17

Rename the csv before it gets added into list and rename their column names to be lower case and get rid of symbols. Hardcode mv = "mv '{0}' {1}".format(csv,new_directory) to new_csv_name = str(os.getcwd() + '/' + new_directory + '/' + csv).

🐢 10/18

Can now import any csv into Postgres DB. Next steps: turn code into functions.
