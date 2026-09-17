from networksequrity.entity.config_entity import TrainingPipelineConfig
from networksequrity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig

from networksequrity.components.data_ingestion import DataIngestion
from networksequrity.components.data_validation import DataValidation
from networksequrity.components.data_transformation import DataTransformation
from networksequrity.components.model_trainer import ModelTrainer
from networksequrity.logging.logger import logging
from networksequrity.exception.exception import NetworkSecurityException

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate Data Ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion() 
        print(dataingestionartifact)
        logging.info('Data Initiation completed')
        logging.info("Initiate Data Validation")
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        datavalidation = DataValidation(dataingestionartifact,datavalidationconfig)
        
        data_validation_artifact = datavalidation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation completed")
        
        logging.info("Intitiating Data Transformation")
        datatransformationconfig = DataTransformationConfig(trainingpipelineconfig)
        datatransformation = DataTransformation(datavalidationconfig,data_transformation_config=datatransformationconfig)  
        datatransformation_artifact = datatransformation.initiate_data_transformation()
        
        print(datatransformation_artifact)
        logging.info("Data transformation Completed")
        
        logging.info("Model Trainer Initiated")
        modeltrainerconfig = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        modeltrainer = ModelTrainer(model_trainer_config=modeltrainerconfig , data_transformation_artifact=datatransformation_artifact)
        model_trainer_artifact = modeltrainer.initiate_model_trainer()
        
        print(model_trainer_artifact)
        logging.info("Model Training Completed")
        
        
    except Exception as e:
        logging.error(NetworkSecurityException(e,sys))
        raise NetworkSecurityException(e,sys)
