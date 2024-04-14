
import os
import sys
from six.moves import urllib
import zipfile
from isd.logger import logging
from isd.exception import isdException
from isd.configuration.s3_operations import S3Operation
from isd.constant.training_pipeline import *
from isd.entity.config_entity import DataIngestionConfig
from isd.entity.artifacts_entity import DataIngestionArtifact



class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig= DataIngestionConfig()):
        try:
            self.data_ingestion_config= data_ingestion_config
            self.s3= S3Operation()
        except Exception as e:
            raise isdException(e,sys)
        
        
    def download_s3_data(self) -> str:
        """
        fetch data from s3
        """
        logging.info("Entering download_s3_data method of DataIngestion component")
        try:
            data_ingestion_dir= self.data_ingestion_config.data_ingestion_dir
            os.makedirs(data_ingestion_dir, exist_ok=True)
            logging.info(f"Downloading data from s3 into {data_ingestion_dir}")
            zip_data_file_path= os.path.join(data_ingestion_dir, self.data_ingestion_config.s3_data_name) # data_ingestion/isd_data_mini.zip
            self.s3.download_object(key= self.data_ingestion_config.s3_data_name, bucket_name= DATA_BUCKET_NAME, filename= zip_data_file_path) 
            logging.info("Exiting download_s3_data method of DataIngestion component")
            return zip_data_file_path
        
        except Exception as e:
            raise isdException(e,sys)
        
        
    def extract_zip_file(self, zip_file_path:str) ->str:
        """
        :param zip_file_path:str
        Extract zip file into data directory
        Function returns None
        """
        logging.info("Entering extract_zip_file method of DataIngestion component")
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            logging.info("Extract zip file into {feature_store_dir}")
            os.system(f"unzip {zip_file_path} -d {feature_store_path}")
            
            logging.info("Exiting extract_zip_file method of DataIngestion component")
            return feature_store_path
        
        except Exception as e:
            raise isdException(e,sys)
        
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates Data Ingestion component; Downloads zip file from s3, Extract zip file into data directory
        Function returns DataIngestionArtifact
        """
        logging.info("Entering initiate_data_ingestion method of DataIngestion component")
        try:
            data_zip_file_path= self.download_s3_data()
            feature_store_path= self.extract_zip_file(zip_file_path=data_zip_file_path)
            
            data_ingestion_artifact = DataIngestionArtifact(data_zip_file_path= data_zip_file_path,
                                                            feature_store_path= feature_store_path)
                
            
            logging.info("Exiting initiate_data_ingestion method of DataIngestion component")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise isdException(e,sys)
        