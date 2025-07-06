from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.path_config import *
from utils.common_functions import read_yaml


if __name__ == "__main__":
    
    ### 1. Data ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    ### 2. Data preprocessing
    data_processor = DataProcessor(TRAIN_FILE_PATH ,TEST_FILE_PATH , PROCESSED_DIR , CONFIG_PATH)
    data_processor.process()


    ### 3. Model Training
    model_training = ModelTraining(PROCESSED_TRAIN_DATA_PATH ,PROCESSED_TEST_DATA_PATH ,MODEL_OUTPUT_PATH)
    model_training.run()
