"""
This benchmark filters female users, groups them by country, and computes the average age of women per country.

The operations are carried out on a dictionary obtained from user data.

Benchmark Steps:
1. Load user data into a dictionary with a specified number of records.
2. Filter female users and group them by country in the dictionary.
3. Find the average age of women per country in the dictionary.
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
dict_users = extract_user_data(num_records=num_records, output_type="dictionary")
logger.info("The required information was loaded successfully")
if is_server:
    socket_client.send_message(message="start")

# -----------
# Operation
# -----------

# Start timer
start_time_dict = time.time()

# Operation 1: Filtering female users and grouping by country in the list
filtered_female_list = [user for user in dict_users if user["gender"] == "female"]
grouped_female_dict = {}
for user in filtered_female_list:
    country = user["country"]
    if country not in grouped_female_dict:
        grouped_female_dict[country] = {"count": 1, "age_sum": user["age"]}
    else:
        grouped_female_dict[country]["count"] += 1
        grouped_female_dict[country]["age_sum"] += user["age"]

# Operation 2: Finding the average age of women per country in the list
average_age_female_dict = {}
for country, data in grouped_female_dict.items():
    average_age_female_dict[country] = data["age_sum"] / data["count"]

# Stop timer
end_time_dict = time.time()
execution_time_dict = end_time_dict - start_time_dict
logger.info(f"Execution Time: {execution_time_dict} seconds")
