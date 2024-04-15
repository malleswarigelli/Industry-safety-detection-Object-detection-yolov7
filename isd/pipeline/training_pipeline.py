import os
import sys
from isd.logger import logging
from isd.exception import isdException
from isd.configuration.s3_operations import S3Operation
from isd.constant.training_pipeline import *
from isd.entity.config_entity import DataIngestionConfig
from isd.entity.artifacts_entity import DataIngestionArtifact
from isd.components.data_ingestion import DataIngestion




class TrainingPipeline:
    def __init__(self):
        self.s3_operations= S3Operation()
        self.data_ingestion_config= DataIngestionConfig()      
        
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entering start_data_ingestion method of TrainingPipeline")
        try:
            logging.info("Getting data from s3")
            data_ingestion= DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            logging.info("Downloaded zip file from s3, unzipped into data_ingestion dir")
            logging.info("Exiting start_data_ingestion method of TrainingPipeline")            
            return data_ingestion_artifact
        
        except Exception as e:
            raise isdException(e, sys)
        
        
        
    
    def run_pipeline(self) -> None:        
        try:
            data_ingestion_artifact= self.start_data_ingestion()
            
            
        except Exception as e:
            raise isdException(e, sys)