import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import pymysql
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error

load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

def read_sql_data():
    logging.info("Reading Sql Database started")
    try:
        database  = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        logging.info("Connection Established",database)
        df =  pd.read_sql_query("Select * from electricity_cost_dataset",database)
        print(df.head())

        return df

    except Exception as e:
        raise CustomException(e,sys)

def save_obj(file_path,obj):
    try:
        dir_path =os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(model,param,cv = 5)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_r2_score = r2_score(y_train,y_train_pred)
            train_model_mae_score = mean_absolute_error(y_train,y_train_pred)
            train_model_rmse_score = np.sqrt(mean_squared_error(y_train,y_train_pred))

            test_model_r2_score = r2_score(y_test,y_test_pred)
            test_model_mae_score = mean_absolute_error(y_test,y_test_pred)
            test_model_rmse_score = np.sqrt(mean_squared_error(y_test,y_test_pred))

            report[list(models.keys())[i]] = test_model_r2_score,test_model_rmse_score,test_model_mae_score
        
        return report
    
    except Exception as e:
        raise CustomException(e,sys)