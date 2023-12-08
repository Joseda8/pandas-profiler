import json
import requests

from src.util.logger import setup_logging

# Set up the logging configuration
logger = setup_logging()

def download_users(num_results=5000):
    url = f"https://randomuser.me/api/?results={num_results}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        users_data = response.json()["results"]

        # Write the data to the JSON file
        file_path = "testing_data/users_data.json"
        with open(file_path, 'w') as json_file:
            json.dump(users_data, json_file, indent=2)

        logger.info(f"Downloaded {num_results} user records and saved to {file_path}.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading data: {e}")

if __name__ == "__main__":
    download_users()
