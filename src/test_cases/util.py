import json
from itertools import cycle, islice
from typing import Dict, Tuple

import pandas as pd

from src.util.cache_data import cache_data
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

def dataframe_to_dict(df: pd.DataFrame) -> Dict:
    """
    Converts a Pandas DataFrame to a dictionary.

    Parameters:
        df (pd.DataFrame): The Pandas DataFrame to be converted.

    Returns:
        dict: The dictionary representation of the DataFrame.
    """
    return df.to_dict("records")

from typing import Union

def extract_user_data(num_records: int, output_type: str) -> Union[pd.DataFrame, Dict]:
    """
    Processes user data by reading it from a JSON file into a DataFrame,
    caching the DataFrame, and converting it to a dictionary, caching the result.

    Parameters:
        num_records (int): The number of records to be processed.
        output_type (str): The desired output type ("dataframe", "dictionary", or "both").

    Returns:
        Union[pd.DataFrame, dict]: Either a DataFrame, a dictionary, or both based on the specified output_type.
    """
    # Assuming cache_data, read_json_to_dataframe, and dataframe_to_dict are defined elsewhere

    # Reading user data into a DataFrame and caching it
    df_users: pd.DataFrame = cache_data(func=read_json_to_dataframe, file_name=f"users_dataframe_{num_records}", cache=True, num_records=num_records)

    if output_type == "dataframe":
        return df_users
    elif output_type == "dictionary":
        # Converting the DataFrame to a dictionary and caching the result
        dict_users: Dict = cache_data(func=dataframe_to_dict, file_name=f"users_dictionary_{num_records}", cache=True, df=df_users)
        del df_users
        return dict_users
    elif output_type == "both":
        # Converting the DataFrame to a dictionary and caching the result
        dict_users: Dict = cache_data(func=dataframe_to_dict, file_name=f"users_dictionary_{num_records}", cache=True, df=df_users)
        return df_users, dict_users
    else:
        raise ValueError("Invalid output_type. Please choose 'dataframe', 'dictionary', or 'both'.")
