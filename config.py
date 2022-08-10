#!/usr/bin/env python
import preprocessing
s3 = {
    "endpoint_url": "https://s3.eu-central-1.wasabisys.com",
    "aws_access_key_id": "xxxxx",
    "aws_secret_access_key": "xxxxxxx",
    "wasabi_bucket": "db-backups"
}
core = {
  "retention_days": "1"
}

psql = {
    "db": "db",
    "pgpassword": "pgpassword",
    "pguser": "postgres"

}
