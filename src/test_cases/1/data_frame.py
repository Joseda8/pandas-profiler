"""
This benchmark filters female users, groups them by country, and computes the average age of women per country in a Pandas DataFrame.

Benchmark Steps:
1. Load user data into a Pandas DataFrame with a specified number of records.
2. Filter female users and group them by country in the DataFrame.
3. Find the average age of women per country in the DataFrame.
4. Measure and log the execution time for each operation.
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
num_records = 2000000
df_users = extract_user_data(num_records=num_records, output_type="dataframe")
logger.info(f"The required information was loaded successfully. Number of records: {num_records}")
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer
start_time = time.time()

# Operation 1: Filtering female users and grouping by country in DataFrame
female_users_df = df_users[df_users['gender'] == 'female']
grouped_female_df = female_users_df.groupby('country').size().reset_index(name='female_count')

# Operation 2: Finding the average age of women per country in DataFrame
average_age_female_df = female_users_df.groupby('country')['age'].mean().reset_index(name='average_age')

# Stop timer
end_time = time.time()
execution_time = end_time - start_time
logger.info(f"Execution Time: {execution_time} seconds")
