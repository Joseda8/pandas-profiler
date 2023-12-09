"""
This benchmark replaces all values in the "password" column with "XXXXXXXX" in a Pandas DataFrame.

Benchmark Steps:
1. Load user data into a Pandas DataFrame with a specified number of records.
2. Replace all values in the "password" column with "XXXXXXXX".
3. Measure and log the execution time for the operation.
"""

import time

from src.util.logger import setup_logging
from src.util.sockets import Client
from src.test_cases.util import extract_user_data


# Set up the logging configuration
logger = setup_logging()

# Init sockets
is_server = True
try:
    socket_client = Client("127.0.0.1", 8888)
except:
    is_server = False
    logger.debug("Test running without profiling")

# Do not measure the execution time of this
num_records = 500000
df_users = extract_user_data(num_records=num_records, output_type="dataframe")
logger.info(f"The required information was loaded successfully. Number of records: {num_records}")
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer
start_time_df = time.time()

# Replace all values in the "password" column with "XXXXXXXX" in the DataFrame
df_users["password"] = "XXXXXXXX"

# Stop timer
end_time_df = time.time()
execution_time_df = end_time_df - start_time_df
logger.info(f"Execution Time: {execution_time_df} seconds")
