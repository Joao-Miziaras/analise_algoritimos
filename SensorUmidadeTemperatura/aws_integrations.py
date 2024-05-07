# IMPORT LIBS
import json
from os import getenv
import logging
import boto3
from boto3.resources.collection import ResourceCollection

session = boto3.Session(
    aws_access_key_id=getenv("345137894335"),
    aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=getenv("AWS_SESSION_TOKEN")
)

s3_client = session.client("s3")

bucket_raw = session.resource("s3").Bucket(getenv("BUCKET_NAME_RAW"))
bucket_raw_name = getenv("BUCKET_NAME_RAW")

bucket_trusted = session.resource("s3").Bucket(getenv("BUCKET_NAME_TRUSTED"))
bucket_trusted_name = getenv("BUCKET_NAME_TRUSTED")

def send_json_to_s3(json_data: dict, json_name: str):    
    s3_client.put_object(
        Bucket=bucket_raw_name,
        Key=json_name,
        Body=json.dumps(json_data).encode('UTF-8')
    )
    print(f"{json_name} - {json_data} sended to raw")

def filter_objects(bucket_name: str, filter: str):
    print("filtering objects")
    objects_found = []
    
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" in response:
        for obj in response["Contents"]:
            if filter in obj["Key"]:
                objects_found.append(obj["Key"])
    else:
        print(f"No objects were found with {filter}")
    
    return objects_found

def exists_folder(bucket: ResourceCollection, path: str):
    objects_in_path = list(bucket.objects.filter(Prefix=path))
    return True if objects_in_path else False

def copy_raw_to_trusted(destiny_path: str, date_id: int):
    objects_to_copy = filter_objects(bucket_raw_name, date_id)
    
    if not exists_folder(bucket_trusted, destiny_path):
        s3_client.put_object(
            Bucket=bucket_trusted_name, 
            Key=destiny_path
        )
        print(f"{destiny_path} created in bucket_trusted")
    
    for object in objects_to_copy:
        source = {"Bucket": bucket_raw_name, "Key": object}
        destination = {"Bucket": bucket_trusted_name, "Key": f"{destiny_path}{object}"}

        s3_client.copy_object(CopySource=source, Bucket=destination["Bucket"], Key=destination["Key"])
        print(f"{object} created in bucket_trusted")