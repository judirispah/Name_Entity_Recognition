import os
import sys
from io import StringIO
from typing import List, Union
from ner.constants import *
import boto3
import pickle
from ner.exception import NerException
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket
from pandas import DataFrame, read_csv
from ner.logger import logging


class S3Operation:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")


    def download_object(self,key, bucket_name, filename):
        bucket = self.s3_resource.Bucket(bucket_name)
        bucket.download_file(Key = key, Filename = filename)    

    def upload_object(self,key, bucket_name, filename):
        bucket = self.s3_resource.Bucket(bucket_name)
        bucket.upload_file(Key = key, Filename = filename) 


    def get_bucket(self, bucket_name: str) -> Bucket:

        """
        Method Name :   get_bucket

        Description :   This method gets the bucket object based on the bucket_name
        
        Output      :   Bucket object is returned based on the bucket name
        """
        logging.info("Entered the get_bucket method of S3Operations class")
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of S3Operations class")
            return bucket

        except Exception as e:
            raise NerException(e, sys) from e
       
    



