"""
Computes the number of registrations per months in a Pandas suitable way
and cutting unused information before processing.

Benchmark Steps:
1. Load user data into a Pandas DataFrame with a specified number of records.
2. Convert the column registered_date to DateTime to extract the year and month.
3. Sum up the value of the nationality and date by using groupby and size.
4. Measure and log the execution time for each operation.
"""

import argparse
import time

import pandas as pd

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
parser.add_argument("--num_records", type=int,
                    help="Number of records to process")
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

# Convert "registered_date" column to datetime
df_users["registered_date"] = pd.to_datetime(df_users["registered_date"].str[:-1])

# Use dt.to_period for year-month grouping
df_users["registration_period"] = df_users["registered_date"].dt.to_period("M")

# Group by nationality and registration_period, then count the occurrences
df_country_year_month_registration = df_users.groupby(["nationality", "registration_period"]).size().reset_index(name="count")

# Stop timer
end_time = time.time()
execution_time = end_time - start_time
logger.info(f"Execution Time: {execution_time} seconds")
