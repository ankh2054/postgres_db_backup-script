#!/usr/bin/env python
import preprocessing
s3 = {
    "endpoint_url": "https://s3.eu-central-1.wasabisys.com",
    "aws_access_key_id": "",
    "aws_secret_access_key": "",
    "wasabi_bucket": "misst-backups"
}
core = {
  "retention_days": "1"
}

psql = {
    "db": "missingwax",
    "pgpassword": "pgpassword",
    "pguser": "postgres"

}
