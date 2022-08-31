import boto3 
import config as cfg
import time

# todays\'s epoch
tday = time.time()
retention = cfg.core["retention_days"]
duration = 86400*int(retention) - 100 #1 days in epoch seconds 
#checkpoint for deletion
expire_limit = tday - duration #duration # Take todays time and deduct one day, if the file is older than that then delete.
print(expire_limit)
# initialize s3 client
file_size = [] #just to keep track of the total savings in storage size


endpoint = cfg.s3["endpoint_url"]
aws_access_key = cfg.s3["aws_access_key_id"]
aws_secret_key = cfg.s3["aws_secret_access_key"]
wasabi_bucket = cfg.s3["wasabi_bucket"]

s4 = boto3.client('s3',
endpoint_url = endpoint,
aws_access_key_id = aws_access_key,
aws_secret_access_key = aws_secret_key)


## Multiple chains - add additional argument, bucketname, version (to be applied as metadata)
def wasabiuploadfile(localfile,remotefile):
    s4.upload_file(
        localfile, wasabi_bucket, remotefile,
        ExtraArgs={
            #'ACL': 'public-read'
            #'ContentType': 'application/gzip'
            }
    )

#works to only get us key/file information
def get_key_info(bucket):

    key_names = []
    file_timestamp = []
    file_size = []
    kwargs = {"Bucket": bucket}
    while True:
        response = s4.list_objects_v2(**kwargs)
        for obj in response["Contents"]:
            # exclude directories/folder from results. Remove this if folders are to be removed too
            if "." in obj["Key"]:
                key_names.append(obj["Key"])
                file_timestamp.append(obj["LastModified"].timestamp())
                file_size.append(obj["Size"])
        try:
            # S3 only returns first 1000, so if more is available a ContinuationToken will be returned.
            # S3 expects you to provide  NextContinuationToken kn your response.
            # So this tests whether we can provide this token.
            # If not we will receive a keyerror.
            kwargs["ContinuationToken"] = response["NextContinuationToken"]
        # If we receive this keyerror, break.
        except KeyError:
            break
    # Append the information to a key_info dict.
    key_info = {
        "key_path": key_names,
        "timestamp": file_timestamp,
        "size": file_size
    }
    return key_info

# connect to s3 and delete the file
def delete_s3_file(file_path, bucket):
    print(f"Deleting {file_path}")
    s4.delete_object(Bucket=bucket, Key=file_path)
    return True

def check_timestamp(fs, limit=expire_limit):
    # Is timestamp of bucket file older than retention
    if fs < limit:
        print(f' File timestamp {fs}')
        print(f'Time limit {limit}')
        return True


def delete_files():
    bucket = wasabi_bucket
    s3_file = get_key_info(bucket)
    # i is the counter 
    for i, fs in enumerate(s3_file["timestamp"]):
        file_expired = check_timestamp(fs)
        if file_expired: #if True is recieved
            delete_s3_file(s3_file["key_path"][i], bucket)