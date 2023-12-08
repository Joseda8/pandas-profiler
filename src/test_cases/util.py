import json
from itertools import cycle, islice

import pandas as pd

from src.util.logger import setup_logging

# Set up the logging configuration
logger = setup_logging()

def read_json_to_dataframe(file_path="testing_data/users_data.json", num_records=None):
    """
    Reads a specific JSON file structure and stores its content in a Pandas DataFrame.

    Parameters:
        file_path (str): The path to the JSON file. Default is "src/test_cases/users_data.json".
        num_records (int): The number of records to retrieve. If None, retrieves all records.

    Returns:
        pd.DataFrame: The Pandas DataFrame containing the data from the specific JSON file structure.
                     Returns None if the file is empty or an error occurs.
    """
    try:
        records = []
        with open(file_path, "r") as json_file:
            # Extract the data from the JSON structure
            records = json.load(json_file)

        # If num_records is specified, adjust the records accordingly
        if num_records is not None:
            # If num_records is less than the total number of records, cut the list
            if num_records < len(records):
                records = records[:num_records]
            # If num_records is more than the total number of records, add duplicates
            elif num_records > len(records):
                records = list(islice(cycle(records), num_records))

        # Flatten the nested structure for each record
        flat_records = []
        for record in records:
            flat_record = {
                "gender": record.get("gender"),
                "title": record.get("name", {}).get("title"),
                "first_name": record.get("name", {}).get("first"),
                "last_name": record.get("name", {}).get("last"),
                "street_number": record.get("location", {}).get("street", {}).get("number"),
                "street_name": record.get("location", {}).get("street", {}).get("name"),
                "city": record.get("location", {}).get("city"),
                "state": record.get("location", {}).get("state"),
                "country": record.get("location", {}).get("country"),
                "postcode": record.get("location", {}).get("postcode"),
                "latitude": record.get("location", {}).get("coordinates", {}).get("latitude"),
                "longitude": record.get("location", {}).get("coordinates", {}).get("longitude"),
                "timezone_offset": record.get("location", {}).get("timezone", {}).get("offset"),
                "timezone_description": record.get("location", {}).get("timezone", {}).get("description"),
                "email": record.get("email"),
                "username": record.get("login", {}).get("username"),
                "password": record.get("login", {}).get("password"),
                "dob": record.get("dob", {}).get("date"),
                "age": record.get("dob", {}).get("age"),
                "registered_date": record.get("registered", {}).get("date"),
                "registered_age": record.get("registered", {}).get("age"),
                "phone": record.get("phone"),
                "cell": record.get("cell"),
                "picture_large": record.get("picture", {}).get("large"),
                "picture_medium": record.get("picture", {}).get("medium"),
                "picture_thumbnail": record.get("picture", {}).get("thumbnail"),
                "nationality": record.get("nat"),
            }
            flat_records.append(flat_record)

        # Convert the flat records to a Pandas DataFrame
        df = pd.DataFrame(flat_records)

        logger.info(f"Read {len(df)} records from {file_path}.")
        return df

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error reading JSON file: {e}")
        return None

def dataframe_to_dict(df):
    """
    Converts a Pandas DataFrame to a dictionary.

    Parameters:
        df (pd.DataFrame): The Pandas DataFrame to be converted.

    Returns:
        dict: The dictionary representation of the DataFrame.
    """
    return df.to_dict()
