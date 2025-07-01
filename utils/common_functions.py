import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the given path")
        
        with open(file_path) as yaml_file :
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config
        
    except Exception as e :
        logger.error("Error while reading YAML file")
        raise CustomException("Failed to read YAML file" , e)
    



def read_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e :
        logger.error("Error while reading data")
        raise CustomException("Failed to read data" , e)
    

def target_encoding(df, encode_col ,target_col,encoded_col_name):
    'This function is replacing the encode_col with a one of [low , mediun , high] bins'
    
    means = df.groupby(encode_col)[target_col].mean()  
    bins = [-0.2 , 0.12 , 0.26 , 0.4]
    cars_bin=['low','Medium','high']
    df[encoded_col_name] = pd.cut(df[encode_col].map(means)  ,bins,right=False,labels=cars_bin )
    df.drop(encode_col , axis = 1 , inplace = True)
    return df