import requests
import json
import ast
import pandas as pd
import pycountry
from datetime import datetime, date
from sqlalchemy import create_engine
from datetime import datetime
import np
import cx_Oracle   # pip install cx_Oracle
from sys import exit

# Replace with your Oracle database connection details
USERNAME = "RM95511"
PASSWORD = "210696"
HOST = "oracle.fiap.com.br"
PORT = "1521"
SID = "ORCL"
TARGET_TABLE = 'FBI_INTERPOL_WANTED_CRIMINALS'
HISTORY_TABLE = 'FBI_INTERPOL_WANTED_CRIMINALS_HISTORY'

# Install Oracle Client https://www.oracle.com/database/technologies/instant-client/downloads.html
# Copy the address where the instant client was unzipped
lib_dir = r"C:\Users\cgodevs\Downloads\archived\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11"

FBI_DATABASE_NAME = 'FBI_CRIMINALS_DATABASE'
INTERPOL_DATABASE_NAME = 'INTERPOL_CRIMINALS_DATABASE'

# ------------------------------ UTILITIES --------------------------------
def format_date(date_str):
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return str(date_str)  # Return the original value as string if it's not a valid date    

def list_to_string(a_list):
    try:
        the_list = ast.literal_eval(a_list)
        joined_string = '; '.join(the_list)
        return joined_string
    except:
        return a_list         

def add_html_paragraph_tags(string):
    strings_with_tags = '<p>' + string + '</p>'
    return strings_with_tags

def get_country_name(country_id):  # 2 letters country code
    try:
        country_obj = pycountry.countries.get(alpha_2=country_id)
        if country_obj != None: 
            return country_obj.name
        return country_id
    except:
        return country_id     

def transform_float_feet_height_to_cm_string(h):
    try:
        feet = int(h / 10)
        inches = int(h % 10)

        feet_cm = feet * 30.48
        inches_cm = inches * 2.54
        
        meters = float(feet_cm + inches_cm) / 100
        
        meters_str = f"{meters:.2f}"
        return meters_str
    except:
        return h   

def get_age_from_date_of_birth(date_string):
    date_format = "%B %d, %Y"
    try:
        date_then = datetime.strptime(date_string, date_format).date()
        current_date = date.today()
        age_in_years = str(int((current_date - date_then).days / 365.25)) + ' years old'  # Account for leap years
        return age_in_years
    except:
        return ''           

def SQL_CREATE_STATEMENT_FROM_DATAFRAME(source_df, target_table_name):
    only_text_data_type_df = source_df.astype(str)
    sql_text = pd.io.sql.get_schema(only_text_data_type_df, target_table_name)   
    oracle_clean_statement = sql_text.replace('\"', '').replace('TEXT', 'VARCHAR2(4000)')
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
        
# --------------------------- Connecting to Database --------------------------------

try:
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    dsn = cx_Oracle.makedsn(HOST, PORT, sid=SID)
    connection = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsn)
    cursor = connection.cursor()
except:  
    print('A connection error happened. Code will be exited.')
    pass

# --------------------------- Get FBI Database to DataFrame --------------------------------

fbi_wanted_df = pd.DataFrame()
try:  # Check if table exists
    fbi_wanted_df = pd.read_sql(f'SELECT * FROM {FBI_DATABASE_NAME}', connection)
except Exception as e:
    print(e)    
    print(f'Table {FBI_DATABASE_NAME} could not be retrieved, code will be exited.')
    exit()

# --------------------------- Get Interpol Database to DataFrame --------------------------------

interpol_wanted_df = pd.DataFrame()
try:  # Check if table exists
    interpol_wanted_df = pd.read_sql(f'SELECT * FROM {INTERPOL_DATABASE_NAME}', connection)
except Exception as e:
    print(e)    
    print(f'Table {INTERPOL_DATABASE_NAME} could not be retrieved, code will be exited.')
    exit()

# -------------------- Transforming and uniting data from both sources ------------------------

interpol_wanted_df['wanted_origin'] = 'INTERPOL'
fbi_wanted_df['wanted_origin'] = 'FBI'    

interpol_wanted_df.columns = [column.lower() for column in interpol_wanted_df.columns]
fbi_wanted_df.columns = [column.lower() for column in fbi_wanted_df.columns]

fbi_wanted_df.rename(
    columns={
        'scars_and_marks':'distinguishing_marks',
        'caution':'charges',
        'eyes':'eyes_color',
        'hair':'hair_color'
    }, 
    inplace=True
)

interpol_wanted_df.rename(
    columns={
        'date_of_birth':'dates_of_birth_used',
        'charge': 'charges',
        'sex_id': 'sex',
        'country_of_birth_id': 'nationality',
        'eyes_colors_id':'eyes_color',
        'hairs_id':'hair_color',
        'languages_spoken_ids': 'languages'
    }, 
    inplace=True
)

interpol_wanted_df['dates_of_birth_used'] = pd.to_datetime(interpol_wanted_df['dates_of_birth_used'])
interpol_wanted_df['dates_of_birth_used'] = interpol_wanted_df['dates_of_birth_used'].apply(format_date)
interpol_wanted_df['age_range'] = interpol_wanted_df['dates_of_birth_used'].apply(get_age_from_date_of_birth)
fbi_wanted_df['dates_of_birth_used'] = fbi_wanted_df['dates_of_birth_used'].apply(list_to_string)

interpol_wanted_df['charges'] = interpol_wanted_df['charges'].apply(add_html_paragraph_tags)

fbi_wanted_df['aliases'] = fbi_wanted_df['aliases'].apply(list_to_string)
interpol_wanted_df['aliases'] = (interpol_wanted_df['forename'] + ' ' + interpol_wanted_df['name']).str.title()
interpol_wanted_df['forename'] = interpol_wanted_df['forename'].str.title()
interpol_wanted_df['name'] = interpol_wanted_df['name'].str.title()

sex_mapping = {'M': 'Male', 'F': 'Female'}
interpol_wanted_df['sex'] = interpol_wanted_df['sex'].map(sex_mapping)

interpol_wanted_df['eyes_color'] = interpol_wanted_df['eyes_color'].apply(list_to_string)
interpol_wanted_df['hair_color'] = interpol_wanted_df['hair_color'].apply(list_to_string)

fbi_wanted_df['height_max'] = fbi_wanted_df['height_max'].apply(transform_float_feet_height_to_cm_string)
fbi_wanted_df['height_min'] = fbi_wanted_df['height_min'].apply(transform_float_feet_height_to_cm_string)
fbi_wanted_df['height'] = fbi_wanted_df['height_min'] + ';' + fbi_wanted_df['height_max']

interpol_wanted_df['languages'] = interpol_wanted_df['languages'].apply(list_to_string)
fbi_wanted_df['languages'] = fbi_wanted_df['languages'].apply(list_to_string)

interpol_wanted_df['nationality'] = interpol_wanted_df['nationality'].apply(get_country_name)
interpol_wanted_df['issuing_country_id'] = interpol_wanted_df['issuing_country_id'].apply(get_country_name)
fbi_wanted_df['issuing_country_id'] = 'United States of America'

fbi_wanted_df['field_offices'] = fbi_wanted_df['field_offices'].apply(list_to_string)
fbi_wanted_df['occupations'] = fbi_wanted_df['occupations'].apply(list_to_string)
fbi_wanted_df['possible_countries'] = fbi_wanted_df['possible_countries'].apply(list_to_string)
fbi_wanted_df['possible_states'] = fbi_wanted_df['possible_states'].apply(list_to_string)
fbi_wanted_df['subjects'] = fbi_wanted_df['subjects'].apply(list_to_string)
interpol_wanted_df['images'] = interpol_wanted_df['images'].apply(lambda item: [item])

merged_df = pd.concat([interpol_wanted_df, fbi_wanted_df], axis=0, ignore_index=True)

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
merged_df['analyzed_at'] = timestamp

merged_df.replace(0, np.nan, inplace=True)
merged_df.replace("nan", np.nan, inplace=True)

print('Success! Finished transforming and uniting data into a single dataframe.')


# -------------------------------------- CONNECT TO ORACLE DATABASE --------------------------------------
try:
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except:  # may have been initialized already
    pass

dsn = cx_Oracle.makedsn(HOST, PORT, sid=SID)
connection = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsn)
cursor = connection.cursor()


# -------------------------------------- WRITE TO PRODUCTION TABLE --------------------------------------
try:  # Check if table exists
    pd.read_sql(f'SELECT * FROM {TARGET_TABLE}', connection)
except:
    try:
        cursor.execute(SQL_CREATE_STATEMENT_FROM_DATAFRAME(interpol_wanted_df, TARGET_TABLE))
        print(f'Table {TARGET_TABLE} created')
    except Exception as e:
        print(f'Table {TARGET_TABLE} not created')
        print(e)
finally:
    try:
        # Delete all records previously written
        cursor.execute(f'DELETE FROM {TARGET_TABLE}')

        # Write the DataFrame to Oracle database 
        insert_statements = SQL_INSERT_STATEMENT_FROM_DATAFRAME(interpol_wanted_df, TARGET_TABLE)
        for statement in insert_statements:
            try:
                cursor.execute(statement)
                connection.commit()  # Commit the changes
            except Exception as e:
                print(e)
        print(f'Done writing to {TARGET_TABLE}')

    except Exception as e:
        print(e)


# -------------------------------------- WRITE TO HISTORY TABLE --------------------------------------
try:  # Check if table exists
    pd.read_sql(f'SELECT * FROM {HISTORY_TABLE}', connection)
except:
    try:
        cursor.execute(SQL_CREATE_STATEMENT_FROM_DATAFRAME(interpol_wanted_df, HISTORY_TABLE))
        print(f'Table {HISTORY_TABLE} created')
    except Exception as e:
        print(f'Table {HISTORY_TABLE} not created')
        print(e)
finally:
    try:
        # Write the DataFrame to Oracle database 
        insert_statements = SQL_INSERT_STATEMENT_FROM_DATAFRAME(interpol_wanted_df, HISTORY_TABLE)
        for statement in insert_statements:
            try:
                cursor.execute(statement)
                connection.commit()  # Commit the changes
            except Exception as e:
                print(e)
        print(f'Done writing to {HISTORY_TABLE}.')

    except Exception as e:
        print(e)

cursor.close()  # Close the cursor
connection.close()