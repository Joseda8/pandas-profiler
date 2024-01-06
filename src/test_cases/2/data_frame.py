"""
This benchmark identifies the users within the age group of 36 to 50.

Benchmark Steps:
1. Load user data into a Pandas DataFrame with a specified number of records.
2. Find the users who's age is greater than 35 and less or equal to 50.
3. Measure the execution time for the operation.
"""

import argparse
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
    logger.debug("\nTest running without profiling")

# Use argparse to get num_records from the terminal
parser = argparse.ArgumentParser(description="Perform a test.")
parser.add_argument("--num_records", type=int, required=True, help="Number of records to process")
args = parser.parse_args()

# Extract data
num_records = args.num_records
df_users = extract_user_data(num_records=num_records, output_type="dataframe")
logger.info(f"The required information was loaded successfully. Number of records: {num_records}")

# Start program
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer
start_time = time.time()


# Identify users between 36 to 50
df_adult_users = df_users[(df_users['age'] > 35) & (df_users['age'] <= 50)]



# Stop timer
end_time = time.time()
execution_time = end_time - start_time
logger.info(f"Execution Time: {execution_time} seconds")
