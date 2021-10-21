# csv_postgres_connector

## About:

Uploads one or multiple CSVs into postgres DB at a time. Just clone this repo, add your csv into the folder, modify main.py, and run it.

Code can be reused for other DBs by creating function similar to connect_to_postgres() in functions.py or check out my other repo "csv_mysql_connecter"

## Goals:

1. Connect to Postgres using psycopg2
2. Import multiple csv's into a Postgres DB at a time

## Progress tracker:
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

Created functions and added to a .py file. Can now import multiple csv into Postgres DB at a time!

🐢 10/20

Made code reusable. Done!
