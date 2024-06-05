import os
import sys
from zipfile import ZipFile
from ner.configuration.s3connector import S3Operation
from ner.constants import *
from ner.entity.artifact_entity import DataIngestionArtifacts
from ner.entity.config_entity import DataIngestionConfig
from ner.exception import NerException
from ner.logger import logging

class DataIngestion:
    def __init__(
        self, data_ingestion_config: DataIngestionConfig, aws:S3Operation) -> None:
        self.data_ingestion_config = data_ingestion_config
        self.aws=aws

    def get_data_from_aws(self, bucket_name: str, file_name: str, key: str) -> ZipFile:
        logging.info("Entered the get_data_from_aws method of data ingestion class")
        try:
            self.aws.download_object(bucket_name=bucket_name,filename=file_name,key=key)

            logging.info("Exited the get_data_from_aws method of data ingestion class")

        except Exception as e:
            raise NerException(e, sys) from e
        

    def extract_data(self, input_file_path: str, output_file_path: str) -> None:
        logging.info("Entered the extract_data method of Data ingestion class")
        try:
            # loading the temp.zip and creating a zip object
            with ZipFile(input_file_path, "r") as zObject:

                # Extracting all the members of the zip
                # into a specific location.
                zObject.extractall(path=output_file_path)
            logging.info("Exited the extract_data method of Data ingestion class")

        except Exception as e:
            raise NerException(e, sys) from e 



    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info(
            "Entered the initiate_data_ingestion method of data ingestion class"
        )
        try:
            # Creating Data Ingestion Artifacts directory inside artifacts folder
            os.makedirs(
                self.data_ingestion_config.data_ingestion_artifacts_dir, exist_ok=True
            )
            logging.info(
                f"Created {os.path.join(self.data_ingestion_config.data_ingestion_artifacts_dir)} directory."
            ) 

            self.get_data_from_aws(bucket_name=BUCKET_NAME,key=AWS_DATA_FILE_NAME,file_name=self.data_ingestion_config.aws_file_path) 
            logging.info(
                f"Got the file from AWS cloud storage. File name - {os.path.join(self.data_ingestion_config.aws_file_path)}"

            )

            # Extracting the data file   
            self.extract_data(
                input_file_path=self.data_ingestion_config.aws_file_path,
                output_file_path=self.data_ingestion_config.csv_file_path,
            ) 
            
            logging.info(f"Extracted the data from zip file.")


            data_ingestion_artifact = DataIngestionArtifacts(
                zip_data_file_path=self.data_ingestion_config.aws_file_path,
                csv_data_file_path=self.data_ingestion_config.csv_output,
            )
            logging.info("Exited the initiate_data_ingestion method of data ingestion class")
            return data_ingestion_artifact

        except Exception as e:
            raise NerException(e, sys) from e
       

    
