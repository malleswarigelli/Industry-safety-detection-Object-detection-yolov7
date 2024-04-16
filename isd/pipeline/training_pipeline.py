import os
import sys
from isd.logger import logging
from isd.exception import isdException
from isd.configuration.s3_operations import S3Operation
from isd.constant.training_pipeline import *
from isd.entity.config_entity import DataIngestionConfig, DataValidationConfig
from isd.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from isd.components.data_ingestion import DataIngestion
from isd.components.data_validation import DataValidation



class TrainingPipeline:
    def __init__(self):
        self.s3_operations= S3Operation()
        self.data_ingestion_config= DataIngestionConfig()      
        self.data_validation_config= DataValidationConfig()
    
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
        
        
    def start_data_validation(self, 
                              data_ingestion_artifact: DataIngestionArtifact
                              ) -> DataValidationArtifact:
        logging.info("Entering start_data_validation method of TrainingPipeline")
        try:
            data_validation = DataValidation(
                data_ingestion_artifact= data_ingestion_artifact,
                data_validation_config= self.data_validation_config,
            )

            data_validation_artifact= data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")

            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
            
        except Exception as e:
            raise isdException(e, sys)    
    
    def run_pipeline(self) -> None:        
        try:
            data_ingestion_artifact= self.start_data_ingestion()
            data_validation_artifact= self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
        except Exception as e:
            raise isdException(e, sys)