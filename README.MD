# PSQL backup using python

Python script that takes a backup of a PSQL database and copies to a S3 bucket.

### Python dependancies required
boto3


### Install 

1. Install python dependancies
2. Copy files to chosen folder
3. Update cron to point to psql_backup.py
4. Update wasabiconfig.py with necessary information.


#### Wasabiconfig.py

- **endpoint_url:** Wasabi endpoint URL for your bucket 
- **aws_access_key_id:** Wasabi/S3 access_key
- **aws_secret_access_key:** Wasabi/S3 secret_key
- **retention_days:** Retention days for files host in the Wasabi/S3 bucket. The pytnon script will delete files older than days specified.
- **db:** Database to backup
- **pguser:** Psql user 
- **pgpassword:** Psql password of user

