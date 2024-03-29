import argparse
import csv
import os
import psutil
import time

from datetime import datetime

from src.util.logger import setup_logging
from src.util.sockets import Server

# Set up the logging configuration
logger = setup_logging()

class SystemStatsCollector:
    def __init__(self, csv_file_path: str, file_profiled: str):
        """
        Initializes the SystemStatsCollector class.

        This class measures the next stats:
            - CPU usage (%)
            - CPU usage per core (%)
            - Usage of physical RAM (%, GB)
            - Usage of swap memory (%, GB)
        """
        # Get the current date and time as a string
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

        self._start_time = time.time()
        self._csv_file_name = f"{csv_file_path}_{file_profiled}_{current_datetime}"
        self._csv_file_path = f"results/{self._csv_file_name}.csv"
        self._num_cpu_cores = psutil.cpu_count(logical=False)
        self._file_profiled = file_profiled
        self._socket_server = Server("127.0.0.1", 8888)

        # Constants
        self._col_name_timestamp = "timestamp"
        self._col_name_cpu_usage = "cpu_usage"
        self._col_name_cpu_cores = [f"cpu_{idx}" for idx in range(self._num_cpu_cores)]
        self._col_name_ram_usage = "ram_usage"
        self._col_name_ram_used = "ram_used"
        self._col_name_disk_swap_usage = "disk_swap_usage"
        self._col_name_disk_swap_used = "disk_swap_used"
        self._col_name_program_running = "program_running"

    def is_program_running(self, program_name: str, last_state: bool) -> bool:
        """
        Check if a program with a specific name is currently running.

        Parameters:
            program_name (str): The name of the program to check.
            last_state (bool): Last state of the program execution detection.

        Returns:
            bool: True if the program is running, False otherwise.
        """
        is_running = False

        # Iterate through the list of processes and retrieve their PIDs and names
        for process in psutil.process_iter(["pid", "name"]):
            cmd_arguments = process.cmdline()
            # Check if the process has command line arguments
            if len(cmd_arguments) > 0:
                # Check if the process is a Python script
                is_python = cmd_arguments[0].find("python") != -1

                if is_python:
                    # Extract the script name if it"s a Python script
                    if cmd_arguments[1] == "-m":
                        script_name = cmd_arguments[2]
                    else:
                        script_name = cmd_arguments[1]

                    # Check if the script name matches the specified program name
                    if script_name.find(program_name) != -1:
                        is_running = True
                        if last_state == False:
                            logger.info(f"The program {program_name} was detected...")
                            self._socket_server.wait_for_message(expected_message="start")
                            self._socket_server.stop_server()

        return is_running
    
    def _get_overall_cpu_usage(self):
        """
        Retrieves the overall CPU usage percentage.

        Returns:
            float: Overall CPU usage percentage.
        """
        cpu_percent = psutil.cpu_percent(interval=0.1)
        return cpu_percent

    def _get_cpu_usage_per_core(self):
        """
        Retrieves the CPU usage percentage for each core.

        Returns:
            list: List of CPU usage percentages for each core.
        """
        cpu_percentages = psutil.cpu_percent(interval=0.1, percpu=True)
        return cpu_percentages

    def _get_ram_usage(self):
        """
        Retrieves RAM usage information.

        Returns:
            tuple: Tuple containing RAM usage percentage and used RAM in bytes.
        """
        ram = psutil.virtual_memory()
        return ram.percent, ram.used / (1024 ** 3)

    def _get_disk_usage(self):
        """
        Retrieves disk usage information.

        Returns:
            tuple: Tuple containing disk usage percentage and used disk space in bytes.
        """
        disk = psutil.swap_memory()
        return disk.percent, disk.used / (1024 ** 3)

    def measure_and_write_stats_to_csv(self):
        """
        Measures system statistics and writes them to a CSV file.
        """
        logger.info("Profiling system state before program execution...")
        with open(self._csv_file_path, mode="w", newline="") as csv_file:
            # Combine all column names into a single list for fieldnames
            fieldnames = [self._col_name_timestamp, self._col_name_cpu_usage] + self._col_name_cpu_cores + [
                self._col_name_ram_usage, self._col_name_ram_used, self._col_name_disk_swap_usage, self._col_name_disk_swap_used,
                self._col_name_program_running
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            try:
                last_state = False
                while True:
                    # Verify if program is running
                    is_running = self.is_program_running(program_name=self._file_profiled, last_state=last_state)
                    last_state = is_running
                    # Get system statistics
                    overall_cpu_usage = self._get_overall_cpu_usage()
                    cpu_usage_per_core = self._get_cpu_usage_per_core()
                    ram_percent, ram_used = self._get_ram_usage()
                    disk_percent, disk_used = self._get_disk_usage()
                    timestamp = round(time.time() - self._start_time, 2)

                    # Create a dictionary for the row data
                    row_data = {
                        self._col_name_timestamp: timestamp,
                        self._col_name_cpu_usage: overall_cpu_usage,
                        self._col_name_ram_usage: ram_percent,
                        self._col_name_ram_used: ram_used,
                        self._col_name_disk_swap_usage: disk_percent,
                        self._col_name_disk_swap_used: disk_used,
                        self._col_name_program_running: is_running
                    }

                    # Populate CPU core data dynamically based on the number of cores
                    for idx, cpu_core in enumerate(cpu_usage_per_core):
                        row_data[self._col_name_cpu_cores[idx]] = cpu_core

                    # Write the row to the CSV file
                    writer.writerow(row_data)

                    logger.debug(f"Execution time: {timestamp} seconds")

            except KeyboardInterrupt:
                self._socket_server.stop_server()

            finally:
                # Log total execution time
                end_time = time.time()
                total_execution_time = end_time - self._start_time
                logger.info(f"\nTotal Execution Time: {total_execution_time:.2f} seconds")

                # Ask the user for execution time of the program
                execution_time_input = input("Enter execution time (in seconds): ")
                num_records = input("Enter the number of records used: ")
                
                # Validate the user input
                try:
                    execution_time = float(execution_time_input)
                except ValueError:
                    logger.error("Invalid input. Please enter a valid number.")
                    execution_time = 0.0
                
                # Create or append execution time information to "execution_times.csv"
                exec_times_file_path = "results/execution_times.csv"
                is_file_exists = os.path.isfile(exec_times_file_path)

                with open(exec_times_file_path, mode="a", newline="") as exec_times_file:
                    exec_times_writer = csv.writer(exec_times_file)

                    # If the file doesn't exist, write header
                    if not is_file_exists:
                        exec_times_writer.writerow(["filename", "records", "time"])

                    # Write the data
                    exec_times_writer.writerow([self._csv_file_name, num_records, execution_time])

# -----------------
# Main
# -----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect system stats and write them to a CSV file.")
    parser.add_argument("--csv_prefix", default="system_stats", help="Path to the CSV file for storing system stats.")
    parser.add_argument("--profiled_file", help="Name of the program to profile.")

    args = parser.parse_args()

    stats_collector = SystemStatsCollector(args.csv_prefix, args.profiled_file)
    stats_collector.measure_and_write_stats_to_csv()
