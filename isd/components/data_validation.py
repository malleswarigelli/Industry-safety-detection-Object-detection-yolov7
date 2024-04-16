import os
import sys
import shutil
from isd.logger import logging
from isd.exception import isdException
from isd.constant.training_pipeline import *
from isd.entity.config_entity import DataValidationConfig
from isd.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation():
    def __init__(self, data_validation_config:DataValidationConfig= DataValidationConfig(),
                 data_ingestion_artifact= DataIngestionArtifact
                 ):
        try: 
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_config= data_validation_config
            
        except Exception as e:
            raise isdException(e,sys)
        
    
    def validate_all_files_exist(self) ->bool:
        """
        validate if all files exist in data_ingestion artifact
        """
        logging.info("Entering validate_all_files_exist method of DataValidation component")
        try:
            validation_status= None
            logging.info("List of expected directories, files to be there")
            all_files= os.listdir(self.data_ingestion_artifact.feature_store_path)
            
            for file in all_files:
                if file not in self.data_validation_config.required_files_list:
                    validation_status= False                    
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)                    
                    logging.info("validation_status")
                    with open(self.data_validation_config.validation_status_file_path, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                        
                else:
                    validation_status= True
                    os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)                    
                    logging.info("validation_status")
                    with open(self.data_validation_config.validation_status_file_path, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                        
            logging.info("Exiting validate_all_files_exist method of DataValidation component")
            return validation_status
        
        except Exception as e:
            raise isdException(e,sys)
        
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Initiates Data Validation component; validate if all files exist in data_ingestion artifact
        Function returns DataValidationArtifact 
        """
        logging.info("Entering initiate_data_validation method of DataValidation component")
        
        try:            
            status= self.validate_all_files_exist()
            logging.info("validation status: {status}")
        
            data_validation_artifact= DataValidationArtifact(validation_status=status)
            
            logging.info("Copying isd_data_mini.zip file to root dir for model training since artifacts won't be moved to github")
            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())
                
            logging.info("Exiting initiate_data_validation method of DataValidation component")    
            return data_validation_artifact
        
        except Exception as e:
            raise isdException(e,sys)