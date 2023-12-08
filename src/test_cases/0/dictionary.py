"""
This benchmark replaces all values in the "password" key with "XXXXXXXX" in the dictionary.

Benchmark Steps:
1. Load user data into a dictionary with a specified number of records.
2. Replace all values in the "password" key with "XXXXXXXX".
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
num_records = 2000000
dict_users = extract_user_data(num_records=num_records, output_type="dictionary")
logger.info("The required information was loaded successfully")
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer
start_time_dict = time.time()

# Replace all values in the "password" key with "XXXXXXXX" in the dictionary
for user in dict_users:
    user['password'] = 'XXXXXXXX'

# Stop timer
end_time_dict = time.time()
execution_time_dict = end_time_dict - start_time_dict
logger.info(f"Execution Time: {execution_time_dict} seconds")
