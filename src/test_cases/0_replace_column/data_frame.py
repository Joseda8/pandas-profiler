import time
import pandas as pd

from src.util.cache_data import cache_data
from src.util.logger import setup_logging
from src.test_cases.util import read_json_to_dataframe

# Set up the logging configuration
logger = setup_logging()

# Do not measure the execution time of this
num_records = 500000
df_users: pd.DataFrame = cache_data(func=read_json_to_dataframe, file_name=f"users_dataframe_{num_records}", cache=True, num_records=num_records)

# Start timer for DataFrame
start_time_df = time.time()

# Replace all values in the "password" column with "XXXXXXXX" in the DataFrame
df_users["password"] = "XXXXXXXX"

# Stop timer for DataFrame
end_time_df = time.time()
execution_time_df = end_time_df - start_time_df
logger.info(f"Execution Time: {execution_time_df} seconds")
