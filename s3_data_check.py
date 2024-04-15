from isd.configuration.s3_operations import S3Operation
from isd.constant.training_pipeline import *
import os
import boto3


obj= S3Operation()

bucket = obj.get_bucket(bucket_name=DATA_BUCKET_NAME)
print("S3 bucket name:", bucket)


# 
obj.download_object(key= os.getcwd(), bucket_name=DATA_BUCKET_NAME, filename=DATA_BUCKET_NAME)
print("data found")


# get file name
file_name= obj.get_file_object(bucket_name=DATA_BUCKET_NAME, filename=DATA_BUCKET_NAME)
print(f"file name in {bucket}:", {file_name})