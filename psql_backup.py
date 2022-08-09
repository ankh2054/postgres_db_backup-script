import requests
import json
import time
from datetime import datetime
from subprocess import PIPE,Popen
import subprocess
import wasabi
import wasabiconfig as cfg





PGUSER = cfg.psql["pguser"]
DB = cfg.psql["db"]
DB_PASSWORD = cfg.psql["pgpassword"]
DIR = '/tmp'

def create_filename():
    #Get current date and time
    now = datetime.now()
    # create date string for filename
    dt_string = now.strftime("%d_%m_%Y-%H_%M")
    # Create filename for snapshot using date string
    FILENAME = DB + dt_string + '.sql'
    return FILENAME

def dump_table(dbname,dbuser,database_password,filename):
    command = f'pg_dump --dbname={dbname} ' \
            f'--username={dbuser} ' \
            f'--no-password ' \
            f'--format=c ' \
            f'--file=/tmp/{filename}'
    proc = Popen(command, shell=True, env={
            'PGPASSWORD': database_password
        })
    proc.wait()


def main():
    # create new filename withdate timestamp and suffix of sql
    filename = create_filename()
    # Take DB dump
    dump_table(DB,PGUSER,DB_PASSWORD,filename)
    # Upload file to Wasabi
    wasabi.wasabiuploadfile(f'/tmp/{filename}',filename)
    # delete backup locally
    subprocess.call([ 'rm', f'/tmp/{filename}'])

if __name__ == "__main__":
     main()

# Delete files older than 2 days in bucket specified
wasabi.delete_files()