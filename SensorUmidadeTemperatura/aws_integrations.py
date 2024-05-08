# IMPORT LIBS
import json
from os import getenv
import logging
import boto3
from boto3.resources.collection import ResourceCollection

session = boto3.Session(
    aws_access_key_id="ASIAYOHTNAJUPE3S4ONJ",
    aws_secret_access_key="gHDAvPhgZplZ/Rbxiu9eDfBbF7eKGGLnLXEYJo0s",
    aws_session_token="IQoJb3JpZ2luX2VjEIT//////////wEaCXVzLXdlc3QtMiJHMEUCIQDqUqf4U8IdUkd98iRt4UMkFR7A0Rh9DCplc63LAGId4QIgPVv2QucrqXW7QegyDO6LFrQelMIcup3I6UnLwik8qAIqwQII3f//////////ARACGgw1ODAzMzEwNDU0ODAiDFTIQbRLWo7XliXFLiqVAvkfLCsak0iJpICYRulMyFNtdZQjhAxYDCUjkXVk6MFeuNzmlt0Vawy1FsQnQpRG5WRQem8JFvN9Qa/TlqCfNdprJMqJ10KBlwwydKq+MMtRdJuAZI4PjwOQTxgyfRc4+GF5DMdFrwoVFJAlYFwrQGFiZrEO2E57EKgKEgCKK9Bk9GlOc6soHcZWnSsFezeIwXBfUnturn4608mw8GkXuRd5vsT5m+/84467L79omiH3HS1L6MPs/LNsVWTiIfE0ToQyA5O9/KFHgtEAsgzB3QpOMKTAS5DE1SywSQv55iG1T2GvL9t3X+zWp9MzzylgLMUmylB3uQvPus/YnAWPoJBabaZ3IIENEgmmQNBtNJBheSKh66gwxo/qsQY6nQEKkfTSgNnm5zgYzZ2/SZ/Yph2jflXBWJTxqbtlrg9TeFztPsgVAfMPDmp0UFe8Y+BtIYvmBHdLbfdj6dI0N0raUjGaHMQPQBIhRwbzQwK+csWWf13tLKLpEgMwkoFrVa1oQ+c7tqhgwOAxIworimS1jtVSNUM8vfvMdX3sl8h4Op0f1/XVPiB0RFndo2C+grMLAK0Fcb3U9NLh7LJW"
)

s3_client = session.client("s3")

bucket_raw = session.resource("s3").Bucket("biosentinel-bucket-raw")
bucket_raw_name = "biosentinel-bucket-raw"


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