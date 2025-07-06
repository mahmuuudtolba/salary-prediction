import os
import pandas as pd
import numpy as np
import joblib
from src.logger import get_logger
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from src.custom_exception import CustomException
from sklearn.ensemble import RandomForestClassifier
from config.path_config import *
from utils.common_functions import target_encoding , read_data , read_yaml
from sklearn.preprocessing import OneHotEncoder , StandardScaler
from sklearn.compose import ColumnTransformer


logger = get_logger(__name__)

class DataProcessor:
    def __init__(self , train_path , test_path , processed_dir , config_path ):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        os.makedirs(self.processed_dir , exist_ok=True)



    def preprocess_data(self , df  , stage):
        try:
            logger.info("Starting our data processing step")

            logger.info("Filling missing data")
            # Replace missing values represented by '?'
            df = df.replace(' ?', np.nan)


            # Fill missing values safely
            df['occupation'] = df['occupation'].fillna('Other-service')
            df['native-country'] = df['native-country'].fillna('Other')
            df['workclass'] = df['workclass'].fillna('Other')

            # logger.info("Dropping outliers")

            # age_old = self.config['data_preprocssing']['outlier_values']["age_old"]
            # age_young = self.config['data_preprocssing']['outlier_values']["age_young"]
            # hours = self.config['data_preprocssing']['outlier_values']["hours"]

            # # Drop outliers safely
            # df_old = df[(df['age'] > age_old) & (df['hours-per-week'] >= hours)]
            # df_young = df[(df['age'] <= age_young) & (df['salary'] == ' >50K')]

            # df = df.drop(index=df_old.index)
            # df = df.drop(index=df_young.index)

            logger.info("Target encoding")

            # Clean and encode
            df['native-country'] = df['native-country'].apply(lambda x: x.strip())
            df = target_encoding(df, 'native-country', 'capital-gain', 'native-country-encoded')
            logger.info("Dropping unnecessary columns")
            df = df.drop(columns='education')

            logger.info("Handling categorical and numerical features")
            cat_cols = self.config['data_preprocssing']['categorical_columns']
            num_cols = self.config['data_preprocssing']['numerical_columns']
            X = df.drop(columns = "salary")
            y = df["salary"]

            if stage == "train":

                preprocesser = ColumnTransformer(
                    transformers=[
                        ('num' , StandardScaler() , num_cols),
                        ('cat' , OneHotEncoder(handle_unknown='ignore') , cat_cols)
                        ]
                    ) 
                X_transformed = preprocesser.fit_transform(X).toarray()
                joblib.dump(preprocesser , "./artifacts/preprocessor.pkl")

            elif stage == "test":
                preprocesser = joblib.load("./artifacts/preprocessor.pkl")
                X_transformed = preprocesser.transform(X).toarray()

                
            feature_names = preprocesser.get_feature_names_out()



            df_transformed = pd.DataFrame(X_transformed , columns=feature_names , index=df.index)
            df_transformed['salary'] = np.array([1 if row == ' >50K' else 0 for row in y ])


            return df_transformed
        
        except Exception as e :
            logger.error(f"Error during preprocessing step {e}")
            raise CustomException("Error while preprocessing data" , e)
        

    def select_features(self , df):
        try:
            logger.info("Start our feature selection step")
            X = df.drop(columns='salary')
            y = df["salary"]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)

            # Train the model
            model = RandomForestClassifier(random_state=22)
            model.fit(X_train, y_train)

            # Predict on test set and calculate accuracy
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"RandomForestClassifier Accuracy: {accuracy:.4f}")


            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature':X.columns,
                'importance':feature_importance
            })

            no_of_features = self.config['data_preprocssing']['no_of_features']

            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)
            top_10_features = top_features_importance_df["feature"].head(no_of_features).values
            
            logger.info(f"Feature selected : {top_10_features}")
            
            top_10_df = df[top_10_features.tolist() + ["salary"]]

            logger.info("feature selection completed successfully")

            return top_10_df
        
        except Exception as e :
            logger.error(f"Error during feature selection {e}")
            raise CustomException("Error during feature selection " , e)

    def save_data(self , df , file_path):
        try:
            logger.info("saving our data in processed folder")
            df.to_csv(file_path , index= False)
            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e :
            logger.error(f"Error during saving data {e}")
            raise CustomException("Error during saving data " , e)
        

    def process(self):
        try:
            logger.info("Loading data from RAW directory")
            df_train = read_data(self.train_path)
            df_test = read_data(self.test_path)

            df_train = self.preprocess_data(df_train , stage="train")
            df_test = self.preprocess_data(df_test , stage="test" )


            df_train = self.select_features(df_train)
            df_test = df_test[df_train.columns]

            df_train = self.save_data(df_train , PROCESSED_TRAIN_DATA_PATH)
            df_test = self.save_data(df_test , PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e :
            logger.error(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error during preprocessing pipeline" , e)
        


if __name__ == "__main__" :
    data_processor = DataProcessor(TRAIN_FILE_PATH ,TEST_FILE_PATH , PROCESSED_DIR , CONFIG_PATH)
    data_processor.process()
            



