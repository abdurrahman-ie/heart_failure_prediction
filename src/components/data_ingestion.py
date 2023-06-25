# import necessary library
import sys
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# import custom library
'''
Add the path to the src folder to the sys.path list
This code ("src_path = ...", "sys.path...") adds the 
path to the src folder (relative to the current script's location)
to the sys.path list, allowing Python to locate and import modules from the src folder.
'''
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(src_path)

from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig


'''
This code performs the data ingestion process by reading a CSV file, 
splitting the data into train and test sets, and saving them in specified 
locations. It also logs the steps and handles custom exceptions.

using "@dataclass" helps to directly use class variable
for more info - https://docs.python.org/3/library/dataclasses.html

To store all the output files in "artifacts" folder: =>
DataIngestionConfig class is used to store the paths of different 
data files related to data ingestion
'''

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', "train.csv")
    test_data_path: str=os.path.join('artifacts', "test.csv")
    raw_data_path: str=os.path.join('artifacts', "data.csv")
    '''
    The above 3 (train_data_path, test_data_path, raw_data_path) are class 
    variables within the DataIngestionConfig class.
    Each variable represents a data path and variable type is string (str)

    "os.path.join()" function is used to join the directory name ('artifacts') 
    with the respective file name ('train.csv', 'test.csv', 'data.csv'). 
    This ensures that the paths are constructed correctly, taking into account 
    the operating system's file path conventions.
    '''

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    # To read the data set from local/ remote server
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:
            '''
            Data read from csv file and store in a data frame "df", but it can read from any server.
            '''
            df=pd.read_csv('data\heart.csv')
            logging.info("Read data set as data frame.")

            # Create the artifacts folder to store csv file
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            
            # Convert the data frame "df" into csv file
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            '''
            Split the data set into train & test. For more sure we use "logging.info(") 
            to ensure program works correctly.
            '''
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            '''
            Save the splitted train & test file into artifac folder as csv file.
            '''
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed.")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except CustomException as e:
            raise CustomException(e, sys)

'''
Below code creates an instance of the "DataIngestion" class and calls the 
"initiate_data_ingestion()" method to perform the data ingestion process.
'''
if __name__ == "__main__": 
    '''
    if __name__ == "__main__": checks if the current script is being 
    executed directly as the main program.
    When a Python script is executed as the main program, 
    the value of __name__ is set to "__main__". 
    If the script is imported as a module in another script, 
    the value of __name__ will be the name of the module.
    '''
    obj = DataIngestion()
    train_data, test_data=obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
