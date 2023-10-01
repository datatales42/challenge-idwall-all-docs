import requests
import json
import pandas as pd
import pycountry
from datetime import datetime, date
from sqlalchemy import create_engine
from datetime import datetime
import np
import cx_Oracle   # pip install cx_Oracle

# Replace with your Oracle database connection details
USERNAME = "RM95511"
PASSWORD = "210696"
HOST = "oracle.fiap.com.br"
PORT = "1521"
SID = "ORCL"
TARGET_TABLE = 'INTERPOL_CRIMINALS_DATABASE'

# Install Oracle Client https://www.oracle.com/database/technologies/instant-client/downloads.html
# Copy the address where the instant client was unzipped
lib_dir = r"C:\Users\cgodevs\Downloads\archived\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11"

# ------------------------------ UTILITIES --------------------------------
def remove_keys_from_dict(the_dict: dict, keys: list):
    for key in keys:
        if key in the_dict:
            del the_dict[key]

def walk_json_path(json_obj, *args):
    inner_value = json_obj
    for arg in args:
        try:
            current_value = inner_value.get(arg, '')
            if current_value == {}:
                break
            inner_value = inner_value.get(arg, '')
        except:
            return ''
    return inner_value           

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
        
# --------------------------- CALL INTERPOL API --------------------------------

page = 1
resultPerPage = 100

interpol_wanted_df = pd.DataFrame()
while True:
    response = requests.get('https://ws-public.interpol.int/notices/v1/red', params={'page': page, 'resultPerPage': resultPerPage})
    try:
        interpol_data = json.loads(response.content)
    except:
        break
    page += 1

    # Get all red notices
    red_notices = interpol_data['_embedded']['notices']

    # Get each red notice inner content
    for notice in red_notices:
        try:
            more_details_url = notice['_links']['self']['href']
            more_details_json = json.loads(requests.get(more_details_url, timeout=5).content) 

            # Handle images
            thumbnail_url = walk_json_path(notice, '_links', 'thumbnail', 'href') 
            images_url = walk_json_path(notice, '_links', 'images', 'href')
            try:
                larger_image_url = json.loads(requests.get(images_url).content)['_embedded']['images'][0]['_links']['self']['href']
                images_dict = {'thumb': thumbnail_url, 'large': larger_image_url}  # Set dict to match FBI response keys 
            except:
                images_dict = {}

            # Remove useless keys
            keys_to_remove_from_dict = ['_links', 'thumbnail', '_embedded']
            remove_keys_from_dict(notice, keys_to_remove_from_dict)
            remove_keys_from_dict(more_details_json, keys_to_remove_from_dict)

            full_notices_dict = {**notice, **more_details_json}  # Unpacking dicts into one
            full_notices_dict['images'] = str(images_dict)

            df =  pd.DataFrame([full_notices_dict])

            # Explode JSON columns
            arrest_warrants = pd.concat([pd.json_normalize(record) for record in df['arrest_warrants']], ignore_index=True)
            df = pd.concat([df.drop(columns='arrest_warrants'), arrest_warrants], axis=1)

            interpol_wanted_df = pd.concat([interpol_wanted_df, df], axis=0, sort=True, ignore_index=True)     
        except Exception as e:
            print('An exception happened. Skipping notice: ') 
            print(notice)
            print(e)
            continue

    print(f'Interpol search page is: {page}. Number of rows fetched from Interpol is: {len(interpol_wanted_df)}')
    if page == 3:   # API can only fetch this far
        break          

print('Success! Finished pulling data from INTERPOL API')

# -------------------------------------- CLEANING --------------------------------------

interpol_wanted_df.drop('charge_translation', axis=1, inplace=True)
interpol_wanted_df.drop('nationalities', axis=1, inplace=True)

interpol_wanted_df['wanted_origin_id'] = interpol_wanted_df['entity_id']
interpol_wanted_df.drop('entity_id', axis=1, inplace=True)

# Oracle may understand np.nan values as a string "nan" and not a null value, this is a workaround
interpol_wanted_df = interpol_wanted_df.astype(object).where(pd.notnull(interpol_wanted_df),None)

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
        cursor.execute(SQL_CREATE_STATEMENT_FROM_DATAFRAME(interpol_wanted_df, TARGET_TABLE))
        print('Table created')
    except Exception as e:
        print('Table not created')
        print(e)
finally:
    try:
        # Write the DataFrame to Oracle database 
        insert_statements = SQL_INSERT_STATEMENT_FROM_DATAFRAME(interpol_wanted_df, TARGET_TABLE)
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
