import sys
import os
from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def data_transformation(self):
        """
        This function is responsible for data transformation"""
        try:
            # Define the column transformer for preprocessing
            categorical_features = ['structure type']
            numerical_features = ['site area', 'water consumption', 'resident count','recycling rate','utilisation rate','air qality index','issue reolution time']

            # numerical_features.drop('recycling rate')
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(),numerical_features),
                    ('cat', OneHotEncoder(), categorical_features)
                ]
            )
            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Reading train and test file")

            preprocessing_obj = self.data_transformation()

            # Divide the train df
            input_feature_train_df = train_df.drop(columns=['electricity cost'],axis=1)
            target_feature_train_df = train_df['electricity cost']

            # Divide the test df
            input_feature_test_df = test_df.drop(columns=['electricity cost'],axis=1)
            target_feature_test_df = test_df['electricity cost']

            logging.info('Applying Preprocessing to train and  test dataset')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info(f'Saved preprocessing objet')

            save_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)