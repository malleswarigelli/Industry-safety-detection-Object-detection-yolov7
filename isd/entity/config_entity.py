
import os
from isd.constant.training_pipeline import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)    
    
   
training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir= os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path= os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_FEATURE_DIR_NAME)
    s3_data_name= DATA_INGESTION_S3_DATA_NAME # "isd_data_mini.zip"