# import necessary library
import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# import custom library
from src.exception import CustomException
from src.logger import logging


@dataclass
# using "@dataclass" helps to directly use class variable
# for more info - https://docs.python.org/3/library/dataclasses.html

# To store all the output files in "artifacts" folder: =>
# DataIngestionConfig class is used to store the paths of different data files related to data ingestion 

class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', "train.csv")
    test_data_path: str=os.path.join('artifacts', "test.csv")
    raw_data_path: str=os.path.join('artifacts', "data.csv")
    '''
    The above 3 (train_data_path, test_data_path, raw_data_path) are class variables within the DataIngestionConfig class.
    Each variable represents a data path and variable type is string (str)

    "os.path.join()" function is used to join the directory name ('artifacts') with the respective file name ('train.csv', 'test.csv', 'data.csv'). This ensures that the paths are constructed correctly, taking into account the operating system's file path conventions.
    '''

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    # To read the data set from local/ remote server
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:
            '''
            Here the data read from csv file, but it can read from any server.
            '''
            df=pd.read_csv('data\heart.csv')
            logging.info("Read data set as data frame.")

            # Create the artifacts folder to store csv file
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed.")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except CustomException as e:
            raise CustomException(e, sys)
