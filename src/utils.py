import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dotenv import load_dotenv
import pymysql

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