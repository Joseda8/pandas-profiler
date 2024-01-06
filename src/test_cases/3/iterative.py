"""
Computes the number of registrations per months iterating over the rows
of a Pandas DataFrame.

Benchmark Steps:
1. Load user data into a Pandas DataFrame with a specified number of records.
2. Iterate over the Pandas DataFrame looking for the nationality and registered_date fields.
3. Sum up the value of the nationality and month accordingly.
4. Measure and log the execution time for each operation.
"""

import argparse
import time

from collections import defaultdict
from datetime import datetime

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
parser.add_argument("--num_records", type=int, help="Number of records to process")
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

# Initialize dictionary to store registration counts for each country and month
country_year_month_registration = defaultdict(int)

# Iterate over the DataFrame
for index, row in df_users.iterrows():
    country = row["nationality"]
    registered_date = row["registered_date"]

    # Convert registered_date to datetime object
    registration_datetime = datetime.fromisoformat(registered_date[:-1])

    # Extract country and month from the datetime object
    country_year_month = (country, registration_datetime.year, registration_datetime.month)

    # Increment the count for the specific country and month
    country_year_month_registration[country_year_month] += 1

# Stop timer
end_time = time.time()
execution_time = end_time - start_time
logger.info(f"Execution Time: {execution_time} seconds")
