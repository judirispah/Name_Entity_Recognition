import sys
from typing import Dict
import dill #binary
import pickle
import numpy as np
import yaml
from zipfile import Path
from ner.constants import *
from ner.exception import NerException
from ner.logger import logging

class MainUtils:
    def read_yaml_file(self, filename: str) -> Dict:
        logging.info("Entered the read_yaml_file method of MainUtils class")
        try:
            with open(filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)

        except Exception as e:
            raise NerException(e, sys) from e
        

    @staticmethod
    def dump_pickle_file(output_filepath: str, data) -> None:
        try:
            with open(output_filepath, "wb") as encoded_pickle:
                pickle.dump(data, encoded_pickle)

        except Exception as e:
            raise NerException(e, sys) from e


    @staticmethod
    def load_pickle_file(filepath: str) -> object:
        try:
            with open(filepath, "rb") as pickle_obj:
                obj = pickle.load(pickle_obj)
            return obj

        except Exception as e:
            raise NerException(e, sys) from e  



        def save_numpy_array_data(self, file_path: str, array: np.array) -> str:
          logging.info("Entered the save_numpy_array_data method of MainUtils class")
        try:
            with open(file_path, "wb") as file_obj:
                np.save(file_obj, array)
            logging.info("Exited the save_numpy_array_data method of MainUtils class")
            return file_path

        except Exception as e:
            raise NerException(e, sys) from e
        

        def load_numpy_array_data(self, file_path: str) -> np.array:
         logging.info("Entered the load_numpy_array_data method of MainUtils class")
        try:
            with open(file_path, "rb") as file_obj:
                return np.load(file_obj)

        except Exception as e:
            raise NerException(e, sys) from e
           