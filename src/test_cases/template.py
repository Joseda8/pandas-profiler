import time
from typing import Dict

import pandas as pd

from src.util.cache_data import cache_data
from src.util.logger import setup_logging
from src.test_cases.util import dataframe_to_dict, read_json_to_dataframe

# Set up the logging configuration
logger = setup_logging()


# Do not measure the execution time of this
num_records = 500000
df_users: pd.DataFrame = cache_data(func=read_json_to_dataframe, file_name=f"users_dataframe_{num_records}", cache=True, num_records=num_records)
dict_users: Dict = cache_data(func=dataframe_to_dict, file_name=f"users_dictionary_{num_records}", cache=True, df=df_users)
del df_users
del dict_users
logger.info("The required information was loaded successfully")
input("Press Enter to continue the execution...")

# -----------
# Operation
# -----------

# Start timer for Dictionary
start_time_dict = time.time()


# Code


# Stop timer for Dictionary
end_time_dict = time.time()
execution_time_dict = end_time_dict - start_time_dict
logger.info(f"Execution Time: {execution_time_dict} seconds")
