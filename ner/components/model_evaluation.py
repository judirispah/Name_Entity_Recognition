import os
import sys
import torch
from pandas import DataFrame
from torch.utils.data import DataLoader
from ner.components.model_trainer import DataSequence
from ner.configuration.s3connector import S3Operation
from ner.constants import *
from ner.entity.artifact_entity import (
    DataTransformationArtifacts,
    ModelEvaluationArtifacts,
    ModelTrainingArtifacts,
)
from ner.entity.config_entity import ModelEvalConfig
from ner.exception import NerException
from ner.logger import logging
from ner.utils.utils import MainUtils



class ModelEvaluation:
    def __init__(
        self,
        data_transformation_artifacts: DataTransformationArtifacts,
        model_training_artifacts: ModelTrainingArtifacts,
        model_evaluation_config: ModelEvalConfig,
    ) -> None:
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_training_artifacts = model_training_artifacts
        self.model_evaluation_config = model_evaluation_config
        self.utils = MainUtils()
        self.gcloud = S3Operation


    def evaluate(self, model: object, df_test: DataFrame) -> float:
        try:
            logging.info("Entered the evaluate method of Model evaluation class")
            tokenizer = self.utils.load_pickle_file(
                filepath=self.model_training_artifacts.tokenizer_file_path
            )
            logging.info("Loaded tokenizer")

            labels_to_ids = self.utils.load_pickle_file(
                filepath=self.data_transformation_artifacts.labels_to_ids_path
            )
            logging.info("labels to ids pickle file loaded") 

            test_dataset = DataSequence(
                df=df_test, tokenizer=tokenizer, labels_to_ids=labels_to_ids
            )
            logging.info("Loaded test dataset for evaluation")

            test_dataloader = DataLoader(test_dataset, batch_size=1) 

            use_cuda = torch.cuda.is_available()
            device = torch.device("cuda" if use_cuda else "cpu")

            if use_cuda:
                model = model.cuda()

            total_acc_test = 0.0

            for test_data, test_label in test_dataloader:
                test_label = test_label.to(device)
                mask = test_data["attention_mask"].squeeze(1).to(device)
                input_id = test_data["input_ids"].squeeze(1).to(device)
                _, logits = model(input_id, mask, test_label)

                for i in range(logits.shape[0]):
                    logits_clean = logits[i][test_label[i] != -100]
                    label_clean = test_label[i][test_label[i] != -100]

                    predictions = logits_clean.argmax(dim=1)
                    acc = (predictions == label_clean).float().mean()
                    total_acc_test += acc

            val_accuracy = total_acc_test / len(df_test)

            print(f"Test Accuracy: {val_accuracy: .3f}")

            logging.info("Exited the evaluate method of Model evaluation class")
            return val_accuracy

        except Exception as e:
            raise NerException(e, sys) from e
        

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        try:
            logging.info("Entered the initiate_model_evaluation method of Model evaluation class")

            # Creating Data Ingestion Artifacts directory inside artifacts folder
            os.makedirs(
                self.model_evaluation_config.model_evaluation_artifacts_dir,
                exist_ok=True,
            )
            logging.info(
                f"Created {os.path.basename(self.model_evaluation_config.model_evaluation_artifacts_dir)} directory."
            )

            model = torch.load(self.model_training_artifacts.bert_model_path)
            logging.info("Loaded bert model")

            df_test = self.utils.load_pickle_file(
                filepath=self.data_transformation_artifacts.df_test_path
            )
            logging.info("Loaded Test dataset for evaluation")

            trained_model_accuracy = self.evaluate(model=model, df_test=df_test)
            logging.info(f"The accuracy on test dataset is - {trained_model_accuracy}")


            model_evaluation_artifact = ModelEvaluationArtifacts(
                trained_model_accuracy=trained_model_accuracy) 

            return model_evaluation_artifact

        except Exception as e:
            raise NerException(e, sys) from e   
   
