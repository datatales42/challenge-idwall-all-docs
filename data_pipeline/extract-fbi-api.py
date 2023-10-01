import requests
import json
import pandas as pd
import cx_Oracle   # pip install cx_Oracle

# Replace with your Oracle database connection details
USERNAME = "RM95511"
PASSWORD = "210696"
HOST = "oracle.fiap.com.br"
PORT = "1521"
SID = "ORCL"
TARGET_TABLE = 'FBI_CRIMINALS_DATABASE'

# Install Oracle Client https://www.oracle.com/database/technologies/instant-client/downloads.html
# Copy the address where the instant client was unzipped
lib_dir = r"C:\Users\cgodevs\Downloads\archived\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11"

# -------------------------------------- UTILITIES --------------------------------------

def SQL_CREATE_STATEMENT_FROM_DATAFRAME(source_df, target_table_name):
    only_text_data_type_df = source_df.astype(str)
    sql_text = pd.io.sql.get_schema(only_text_data_type_df, target_table_name)   
    oracle_clean_statement = sql_text.replace('\"', '').replace('TEXT', 'VARCHAR2(4000)').replace('\n','')
    return oracle_clean_statement

def SQL_INSERT_STATEMENT_FROM_DATAFRAME(source_df, target_table_name):
    sql_texts = []
    for index, row in source_df.iterrows():
        columns_str = ', '.join(source_df.columns)
        values_list = [str(value).replace("'", "''") if value is not None else 'NULL' for value in row.values]
        values_str = ', '.join([f"'{value}'" if value != 'NULL' else 'NULL' for value in values_list])
        insert_statement = f"INSERT INTO {target_table_name} ({columns_str}) VALUES ({values_str})"
        sql_texts.append(insert_statement)
    return sql_texts        

# -------------------------------------- CALL FBI API --------------------------------------
# Create an empty DataFrame
fbi_wanted_df = pd.DataFrame()

page = 1
while True:
    response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
    data = json.loads(response.content)

    if data['total'] == 0 or data['items'] == []:
        print('No data left to fetch')
        break

    response_items = data['items']

    # Ensure all keys are present in every dictionary
    all_keys = list(set().union(*(item.keys() for item in response_items)))
    for item in response_items:
        for k in all_keys:
            item.setdefault(k, None)

    # Create a DataFrame
    df = pd.DataFrame(response_items, columns=all_keys)

    # Concatenate the DataFrame to the existing DataFrame
    fbi_wanted_df = pd.concat([fbi_wanted_df, df], axis=0, sort=True, ignore_index=True)
    
    print(f'FBI search page is: {page}')
    page += 1
    if page == 99:     # Loop safety check
        print('Something\'s wrong, page iteration is at 99')
        break     

print(f'Number of rows fetched from FBI is: {len(fbi_wanted_df)}')
print('Success! Finished pulling data from FBI API')


# -------------------------------------- CLEANING --------------------------------------
fbi_wanted_df.drop('path', axis=1, inplace=True)
fbi_wanted_df.drop('legat_names', axis=1, inplace=True)
fbi_wanted_df.drop('locations', axis=1, inplace=True)
fbi_wanted_df.drop('files', axis=1, inplace=True)
fbi_wanted_df.drop('coordinates', axis=1, inplace=True)
fbi_wanted_df.drop('@id', axis=1, inplace=True)
fbi_wanted_df.drop('additional_information', axis=1, inplace=True)
fbi_wanted_df.drop('description', axis=1, inplace=True)
fbi_wanted_df.drop('reward_max', axis=1, inplace=True)
fbi_wanted_df.drop('reward_min', axis=1, inplace=True)

fbi_wanted_df['wanted_origin_id'] = fbi_wanted_df['uid']
fbi_wanted_df.drop('uid', axis=1, inplace=True)

# Oracle may understand np.nan values as a string "nan" and not a null value, this is a workaround
fbi_wanted_df = fbi_wanted_df.astype(object).where(pd.notnull(fbi_wanted_df),None)

# -------------------------------------- SAVE TO ORACLE DATABASE --------------------------------------
try:
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except:  # may have been initialized already
    pass

dsn = cx_Oracle.makedsn(HOST, PORT, sid=SID)
connection = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsn)
cursor = connection.cursor()

try:  # Check if table exists
    pd.read_sql(f'SELECT * FROM {TARGET_TABLE}', connection)
except:
    try:
        cursor.execute(SQL_CREATE_STATEMENT_FROM_DATAFRAME(fbi_wanted_df, TARGET_TABLE))
        print('Table created')
    except Exception as e:
        print('Table not created')
        print(e)
finally:
    try:
        # Delete all records previously written
        cursor.execute(f'DELETE FROM {TARGET_TABLE}')
        # Write the DataFrame to Oracle database 
        insert_statements = SQL_INSERT_STATEMENT_FROM_DATAFRAME(fbi_wanted_df, TARGET_TABLE)
        for statement in insert_statements:
            try:
                cursor.execute(statement)
                connection.commit()  # Commit the changes
            except Exception as e:
                print(e)
        print('Script is finished.')

    except Exception as e:
        print(e)

cursor.close()  # Close the cursor
connection.close()
