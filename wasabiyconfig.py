#!/usr/bin/env python
import preprocessing
s3 = {
    "endpoint_url": "https://s3.eu-central-1.wasabisys.com",
    "aws_access_key_id": "${AWS_ACCESS_KEY_ID}",
    "aws_secret_access_key": "${AWS_SECRET_ACCESS_KEY}",
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
