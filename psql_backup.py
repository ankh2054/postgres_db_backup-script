import psycopg2
from psycopg2 import sql
from datetime import datetime
import wasabi
import os
import json

CONFIG_PATH = '/app/configs.json'
DIR = '/tmp'

def create_filename(db):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y-%H_%M")
    return f"{db}_{dt_string}.sql"

def dump_database(host, dbname, user, password, output_file, bucket_name):
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [row[0] for row in cursor.fetchall()]
    
    with open(output_file, 'w') as f:
        # Dump schema
        cursor.execute("""
            SELECT table_name, column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_schema='public'
        """)
        for table, column, dtype, nullable, default in cursor.fetchall():
            null_constraint = " NOT NULL" if nullable == 'NO' else ""
            default_constraint = f" DEFAULT {default}" if default else ""
            f.write(f"CREATE TABLE {table} ({column} {dtype}{null_constraint}{default_constraint});\n")
        
        # Dump data
        for table in tables:
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
            for row in cursor.fetchall():
                values = ', '.join([f"'{str(value)}'" if value is not None else 'NULL' for value in row])
                f.write(f"INSERT INTO {table} VALUES ({values});\n")
    
    cursor.close()
    conn.close()
    wasabi.wasabiuploadfile(output_file, create_filename(dbname), bucket_name)

def main(configs):    
    for cfg in configs:
        filename = create_filename(cfg['db'])
        output_path = os.path.join(DIR, filename)
        dump_database(cfg['host'], cfg['db'], cfg['user'], cfg['password'], output_path, cfg['bucket'])
        os.remove(output_path)

if __name__ == "__main__":
    with open(CONFIG_PATH) as f:
        configs = json.load(f)
    main(configs)
    # Delete old files for each bucket
    for cfg in configs:
        wasabi.delete_files(cfg['bucket'])