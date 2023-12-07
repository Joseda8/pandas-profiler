import json
import os
import requests

def download_users(num_results=5000):
    url = f"https://randomuser.me/api/?results={num_results}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        users_data = response.json()["results"]

        # Save each user record to a JSON file in src/test_cases
        file_path = "testing_data/users_data.json"
        with open(file_path, "w") as json_file:
            for user in users_data:
                json.dump(user, json_file, indent=2)
                json_file.write("\n")  # Add a newline between records

        print(f"Downloaded {num_results} user records and saved to {file_path}.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")

if __name__ == "__main__":
    download_users()
