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
dict_users = extract_user_data(num_records=num_records, output_type="dictionary")
logger.info(f"The required information was loaded successfully. Number of records: {num_records}")

# Start program
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer
start_time = time.time()


# # Identify users between 0 to 12
young_users = []
for user in dict_users:
    if user["age"] <= 12:
        young_users.append(user)
logger.info(f"Users between 0 to 12: {young_users}")

# Identify users between 13 to 19
teenage_users = []
for user in dict_users:
    if user["age"] > 12 and user["age"] <= 19:
        teenage_users.append(user)
logger.info(f"Users between 13 to 19: {teenage_users}")

# Identify users between 20 to 35
youth_users = []
for user in dict_users:
    if user["age"] > 19 and user["age"] <= 35:
        youth_users.append(user)
logger.info(f"Users between 20 to 35: {youth_users}")

# Identify users between 36 to 50
adult_users = []
for user in dict_users:
    if user["age"] > 35 and user["age"] <= 50:
        adult_users.append(user)
logger.info(f"Users between 36 to 50: {adult_users}")

# Identify users 51 and above
elderly_users = []
for user in dict_users:
    if user["age"] > 50:
        elderly_users.append(user)
logger.info(f"Users 51 and above: {elderly_users}")



# Stop timer
end_time = time.time()
execution_time = end_time - start_time
logger.info(f"Execution Time: {execution_time} seconds")
