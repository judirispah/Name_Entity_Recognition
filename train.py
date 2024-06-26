from ner.pipeline.train_pipeline import TrainPipeline
from ner.exception import NerException
import sys
def training():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

    except Exception as e:
        raise NerException(e, sys) from e


if __name__ == "__main__":
    training()