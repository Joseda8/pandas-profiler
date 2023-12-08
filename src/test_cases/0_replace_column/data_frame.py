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
df_users, _ = extract_user_data(num_records=num_records)
logger.info("The required information was loaded successfully")
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer for DataFrame
start_time_df = time.time()

# Replace all values in the "password" column with "XXXXXXXX" in the DataFrame
df_users["password"] = "XXXXXXXX"

# Stop timer for DataFrame
end_time_df = time.time()
execution_time_df = end_time_df - start_time_df
logger.info(f"Execution Time: {execution_time_df} seconds")
