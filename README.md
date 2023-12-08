# Pandas profiler

## _Collect and record the behavior of Pandas under several scenarios_


# Profiler
The **profiler** is a Python script designed to measure and record various system statistics over time. It collects data such as CPU usage, CPU usage per core, RAM usage, and swap memory usage. The collected data is then stored in a CSV file for further analysis.

## Features

- Measure CPU usage, CPU usage per core, RAM usage, and swap memory usage.
- Record data in a CSV file for easy analysis.
- Profile a specific program to check if it's running.

## Usage

### Command-line Options
- `--csv_prefix`: Prefix of the CSV file for storing system stats. Default is `system_stats`.
- `--profiled_file`: Name of the program to profile. Default is `test_script`.

### Running the Script

First you have to run the profiler with the desired options. For example:
```bash
python3 profiler.py --csv_file system_stats.csv --profiled_file test_script
```

Now run the script to profile, `test_script.py` for the example shown above.

### Exiting the Script
The script runs indefinitely, collecting and writing system statistics to the specified CSV file. To stop the script, use `Ctrl+C`.


## Collected Stats

The script measures the following system statistics:

- **Timestamp**: Time elapsed since the start of execution.
- **Overall CPU Usage**: Percentage of overall CPU usage.
- **CPU Cores Usage**: Percentage of CPU usage for each individual core.
- **RAM Usage**: Percentage of physical RAM usage.
- **Used RAM**: Amount of physical RAM used in gigabytes.
- **Swap Memory Usage**: Percentage of swap memory usage.
- **Used Swap Memory**: Amount of swap memory used in gigabytes.
- **Program Running**: Whether the specified program is currently running.

# Downloader

To download testing data the API `randomuser` is used to download 5000 records and store them in a JSON file in the folder `testing_data`.

Use this script with:

```bash
python3 downloader.py
```
