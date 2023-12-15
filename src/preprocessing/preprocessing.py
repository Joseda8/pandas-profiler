import pandas as pd
from src.preprocessing.util import round_to_significant_decimals
from src.util.logger import setup_logging

# Set up the logging configuration
logger = setup_logging()

class Preprocessing:
    """
    Class for performing data preprocessing tasks.

    """

    def __init__(self):
        """
        Initializes the Preprocessing class.
        """
        pass

    def truncate_decimals(self, input_file_path: str, output_file_path: str) -> None:
        """
        Truncates decimals in the "time" column of a CSV file and saves the modified DataFrame to a new CSV file.

        Parameters:
        input_file_path (str): The path to the input CSV file.
        output_file_path (str): The path to save the preprocessed CSV file.
        """
        try:
            # Load CSV file
            df = pd.read_csv(input_file_path)

            # Truncate decimals in the "time" column to three using the custom rounding function
            df["time"] = df["time"].apply(lambda time: round_to_significant_decimals(number=time, num_significant_decimals=3))

            # Save the modified DataFrame to a new CSV file
            df.to_csv(output_file_path, index=False)

            logger.info(f"Decimals truncated and saved to {output_file_path}")

        except Exception as e:
            logger.error(f"Error during preprocessing: {str(e)}")


if __name__ == "__main__":
    # Initialize the Preprocessing class
    processor = Preprocessing()

    # Specify input and output file paths
    input_path = "results/execution_times.csv"
    output_path = "results/execution_times_preprocessed.csv"

    # Call the truncate_decimals method
    processor.truncate_decimals(input_file_path=input_path, output_file_path=output_path)
