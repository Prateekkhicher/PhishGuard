from networksequrity.constant.training_pipeline import TRAINING_BUCKET_NAME
from networksequrity.components.data_ingestion import DataIngestion
from networksequrity.components.data_validation import DataValidation
from networksequrity.components.data_transformation import DataTransformation
from networksequrity.components.model_trainer import ModelTrainer

from networksequrity.logging.logger import logging

from networksequrity.exception.exception import NetworkSecurityException

import os 
import sys

from networksequrity.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig
)

from networksequrity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)

from networksequrity.cloud.s3_syncer import S3Sync

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.S3sync = S3Sync()
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("START DATA INGESTION")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(f"DATA INGESTION COMPLETED and Artifact : {data_ingestion_artifact}")
            
            return data_ingestion_artifact
        
        except Exception as e:
            # logging.error(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Validation Initiated")
            data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed and Artifact : {data_validation_artifact}")
            
            return data_validation_artifact
            
        except Exception as e:
            # logging.error(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            
            logging.info("Data Transformation Started")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed and Artifact : {data_transformation_artifact}")
            
            return data_transformation_artifact
        
        except Exception as e:
            # logging.error(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)
    
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            logging.info("Model Trainer Initiated")
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            
            logging.info(f"Model Trainer completed and Artifact : {model_trainer_artifact}")
            
            return model_trainer_artifact
        
        except Exception as e:
            # logging.error(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)
    # send local artifact to S3 bucket
    def sync_artifact_to_s3(self):
        '''
        sending all the artifacts( data ingestion , validation , transformation , model trainer Artifact to S3 bucket ( cloud storage))
        '''
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/Artifacts/{self.training_pipeline_config.timestamp}"
            self.S3sync.sync_folder_to_s3(folder_name=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
            logging.info("Artifacts synced to S3")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    #send local model to S3 bucket
    def sync_model_to_s3(self):
        '''
        sending the model to the cloud
        '''
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.S3sync.sync_folder_to_s3(folder_name=self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
            logging.info("Model synced to S3")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def run_pipeline(self):
        '''
        Runs Each process one by one as a pipeline
        '''
        
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            
            self.sync_model_to_s3()
            self.sync_artifact_to_s3()
            return model_trainer_artifact
            
        except Exception as e:
            logging.error(NetworkSecurityException(e,sys))
            raise NetworkSecurityException(e,sys)