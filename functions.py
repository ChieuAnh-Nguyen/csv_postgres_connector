# import os
# import re
# import pandas as pd
# import psycopg2
import os
import re
import pandas as pd
import psycopg2
import postgres_creds as cred
# Since changes were made in cred and our ipynb can't see new changes, we use Importlib to reload the module
import importlib
importlib.reload(cred)

# 1. add csv's in current directory to a list
# re.sub(r'[^\w\.]', '_', csv) substitutes all non word and num characters
def create_csv_list():
    csv_files = []
    for csv in os.listdir(os.getcwd()):
        if '.csv' in csv:
            old_csv_name = str(os.getcwd() + '/' + csv)
            csv = re.sub(r'[^\w\.]', '_', csv).lower()
            # 2. Check cwd, if csv in cwd, move csv to new folder
            new_csv_name = str(os.getcwd() + '/' + csv)
            if os.path.isfile(new_csv_name):
                pass
            else:
                # Rename the file
                os.rename(old_csv_name, new_csv_name)
            csv_files.append(csv)
    return csv_files

# Create new folder in current directory
def change_directory(csv_files,new_directory):
    try:
        os.mkdir(new_directory)
    except:
        pass
    # move files to new directory
    for csv in csv_files:
        mv = "mv '{0}' {1}".format(csv,new_directory)
        os.system(mv)
    return

#Create dictionary with csv name as key and df as value
def create_dict(csv_files, new_directory):
    df_dict = {}
    for csv in csv_files:
        csv_path = str(os.getcwd() + '/' + new_directory + '/' + csv)
        df_dict[csv] = pd.read_csv(csv_path, index_col = 0)
    return df_dict

# cleans column names and changes pd datatypes to sql datatypes
def clean_columns(dataframe):
    dataframe_columns = [re.sub(r'[^\w\.]', '_', column_name).lower() for column_name in dataframe.columns]

# Replacing pd datatypes with sql datatypes
    replacements = {
        'timedelta64[ns]': 'varchar(255)',
        'object': 'varchar(255)',
        'float64': 'float',
        'bool': 'boolean',
        'int64': 'int',
        'datetime64': 'timestamp'}
    replaced_dtypes = dataframe.dtypes.replace(replacements)
    # table schema
    column_dtype = ", ".join("{} {}".format(col_name, dtype) for (col_name, dtype) in zip(dataframe_columns, replaced_dtypes))

    return dataframe_columns, column_dtype

# Creates DB table name
def upload_csv_to_DB(host,user,password,database,dataframe,file_name,dataframe_columns,column_dtype):
    conn = psycopg2.connect(host = host,
    user = user, 
    password = password,
    database = database)
    cursor = conn.cursor()

    db_table_name = file_name.split('.')[0]
    #dataframe.columns as a str
    dataframe_columns_insertable = ', '.join(dataframe_columns)
    # 2. create queries
    drop_table = 'DROP TABLE IF EXISTS ' + db_table_name
    create_table = 'CREATE TABLE ' + db_table_name + " (" + column_dtype + ")"
    insert_into_table = 'INSERT INTO ' + db_table_name + '(' + dataframe_columns_insertable + ')' \
    +' VALUES ( %s' % ', '.join(['%s'] * len(dataframe_columns)) +')'
        
    select_table = 'SELECT * FROM ' + db_table_name

    cursor.execute(drop_table)
    cursor.execute(create_table)
    # 3. create insert into function
    for index, row in dataframe.iterrows():
        cursor.execute(insert_into_table,row)

    conn.commit()

    # 4. Grant access to all users
    cursor.execute('GRANT SELECT, INSERT, UPDATE ON TABLE %s TO PUBLIC' % db_table_name)

    # 4. Show table in DB
    cursor.execute(select_table)
    for each in cursor:
        print(each)
    

    cursor.close()


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

    upload_csv_to_DB(cred.host, cred.user, cred.password, cred.database, dataframe,key , dataframe_columns, column_dtype)
