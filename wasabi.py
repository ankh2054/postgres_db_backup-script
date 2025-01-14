import boto3 
import time


tday = time.time()
retention = 2
duration = 86400*int(retention) - 100 #1 days in epoch seconds 
expire_limit = tday - duration #duration # Take todays time and deduct one day, if the file is older than that then delete.
file_size = [] #just to keep track of the total savings in storage size


# Hardcoded AWS credentials (from your earlier snippet)
s4 = boto3.client('s3',
    endpoint_url="https://s3.eu-central-1.wasabisys.com",
    aws_access_key_id="1J7XQIHHZ6TTMGDVEL1G",
    aws_secret_access_key="2tS8gegOl0dkozbDYwU80Je2MChv0TEGztTiObPr"
)

## Multiple chains - add additional argument, bucketname, version (to be applied as metadata)
def wasabiuploadfile(localfile,remotefile,bucket_name):
    s4.upload_file(
        localfile, bucket_name, remotefile,
        ExtraArgs={
            #'ACL': 'public-read'
            #'ContentType': 'application/gzip'
            }
    )

#works to only get us key/file information
def get_key_info(bucket_name):
    key_names = []
    file_timestamp = []
    file_size = []
    kwargs = {"Bucket": bucket_name}
    while True:
        response = s4.list_objects_v2(**kwargs)
        # Check if 'Contents' is in the response
        if 'Contents' in response:
            for obj in response["Contents"]:
                # exclude directories/folder from results. Remove this if folders are to be removed too
                if "." in obj["Key"]:
                    key_names.append(obj["Key"])
                    file_timestamp.append(obj["LastModified"].timestamp())
                    file_size.append(obj["Size"])
        else:
            print("Bucket is empty.")
            break
        try:
            kwargs["ContinuationToken"] = response["NextContinuationToken"]
        except KeyError:
            break
    key_info = {
        "key_path": key_names,
        "timestamp": file_timestamp,
        "size": file_size
    }
    return key_info

# connect to s3 and delete the file
def delete_s3_file(file_path, bucket_name):
    print(f"Deleting {file_path}")
    s4.delete_object(Bucket=bucket_name, Key=file_path)
    return True

def check_timestamp(fs, limit=expire_limit):
    # Is timestamp of bucket file older than retention
    if fs < limit:
        print(f' File timestamp {fs}')
        print(f'Time limit {limit}')
        return True


def delete_files(bucket_name):
    s3_file = get_key_info(bucket_name)
    # i is the counter 
    for i, fs in enumerate(s3_file["timestamp"]):
        file_expired = check_timestamp(fs)
        if file_expired: #if True is recieved
            delete_s3_file(s3_file["key_path"][i], bucket_name)

