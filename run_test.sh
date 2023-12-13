#!/bin/bash

# Define the module name
module_name="src.test_cases.0.dictionary"

# List of num_records values to try
num_records_list=(1000 10000 100000 200000 500000 1000000 2000000 5000000)

# Loop through each num_records value
for num_records in "${num_records_list[@]}"; do
    # Run the Python command
    python3 -m "$module_name" --num_records "$num_records"

    # Ask for user input to continue
    read -p "Press Enter to continue..."
done
