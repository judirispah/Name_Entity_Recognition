from ner.constants import *
from dataclasses import dataclass
import os

@dataclass
class DataIngestionConfig:
    
    data_ingestion_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR
        )
    aws_file_path:str=os.path.join(data_ingestion_artifacts_dir,AWS_DATA_FILE_NAME)
    csv_file_path:str=os.path.join(data_ingestion_artifacts_dir)
    csv_output:str=os.path.join(data_ingestion_artifacts_dir,CSV_DATA_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR
        )
    labels_to_ids_path: str = os.path.join(
           data_transformation_artifacts_dir, LABELS_TO_IDS_FILE_NAME)
    
    ids_to_labels_path: str = os.path.join(
            data_transformation_artifacts_dir, IDS_TO_LABELS_FILE_NAME)
    
    df_train_path: str = os.path.join(
            data_transformation_artifacts_dir, DF_TRAIN_FILE_NAME
        )
    
    df_val_path: str = os.path.join(
           data_transformation_artifacts_dir, DF_VAL_FILE_NAME
        )
    
    df_test_path: str = os.path.join(
            data_transformation_artifacts_dir, DF_TEST_FILE_NAME
        )
    
    unique_labels_path: str = os.path.join(
           data_transformation_artifacts_dir, UNIQUE_LABELS_FILE_NAME
        )
    
@dataclass
class ModelTrainingConfig:
    
    model_training_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, MODEL_TRAINING_ARTIFACTS_DIR
        )
    bert_model_instance_path: str = os.path.join(
            model_training_artifacts_dir, AWS_MODEL_NAME
        )
    tokenizer_file_path: str = os.path.join(
          model_training_artifacts_dir, TOKENIZER_FILE_NAME
        )
    

@dataclass
class ModelEvalConfig:
   
        model_evaluation_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, MODEL_EVALUATION_ARTIFACTS_DIR
        ) 


@dataclass
class ModelPredictorConfig:
    def __init__(self):
        self.tokenizer_local_path: str = TOKENIZER_FILE_NAME
        self.ids_to_labels_local_path: str = IDS_TO_LABELS_FILE_NAME
        self.best_model_dir: str = BEST_MODEL_DIR
        self.best_model_from_gcp_path: str = os.path.join(BEST_MODEL_DIR)
        self.best_model_path: str = os.path.join(BEST_MODEL_DIR, AWS_MODEL_NAME)

    


    




