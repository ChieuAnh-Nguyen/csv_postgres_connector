import os
import re
import pandas as pd
import psycopg2
# Since changes were made in cred and our ipynb can't see new changes, we use Importlib to reload the module
import importlib
import postgres_creds as cred
importlib.reload(cred)
from functions import *


# Main.py
new_directory = "imported_csv"

# Create list of csv
csv_files = create_csv_list()

# Create new directory and move files
change_directory (csv_files, new_directory)

# Create dict
df_dict = create_dict(csv_files, new_directory)

for key in df_dict:
# value
    dataframe = df_dict[key]
    dataframe_columns, column_dtype = clean_columns(dataframe)

    upload_csv_to_DB(cred.host, cred.user, cred.password, cred.database, dataframe,key, dataframe_columns, column_dtype)
