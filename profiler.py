import argparse
import csv
import psutil
import time


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
        self._start_time = time.time()
        self._csv_file_path = csv_file_path
        self._num_cpu_cores = psutil.cpu_count(logical=False)
        self._file_profiled = file_profiled

        # Constants
        self._col_name_timestamp = "timestamp"
        self._col_name_cpu_usage = "cpu_usage"
        self._col_name_cpu_cores = [f"cpu_{idx}" for idx in range(self._num_cpu_cores)]
        self._col_name_ram_usage = "ram_usage"
        self._col_name_ram_used = "ram_used"
        self._col_name_disk_swap_usage = "disk_swap_usage"
        self._col_name_disk_swap_used = "disk_swap_used"
        self._col_name_program_running = "program_running"

    @staticmethod
    def is_program_running(program_name: str) -> bool:
        """
        Check if a program with a specific name is currently running.

        Parameters:
            program_name (str): The name of the program to check.

        Returns:
            bool: True if the program is running, False otherwise.
        """
        is_running = False

        # Iterate through the list of processes and retrieve their PIDs and names
        for process in psutil.process_iter(['pid', 'name']):
            cmd_arguments = process.cmdline()
            # Check if the process has command line arguments
            if len(cmd_arguments) > 0:
                # Check if the process is a Python script
                is_python = cmd_arguments[0].find("python") != -1

                if is_python:
                    # Extract the script name if it's a Python script
                    if cmd_arguments[1] == "-m":
                        script_name = cmd_arguments[2]
                    else:
                        script_name = cmd_arguments[1]

                    # Check if the script name matches the specified program name
                    if script_name.find(program_name) != -1:
                        is_running = True

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
        with open(self._csv_file_path, mode="w", newline="") as csv_file:
            # Combine all column names into a single list for fieldnames
            fieldnames = [self._col_name_timestamp, self._col_name_cpu_usage] + self._col_name_cpu_cores + [
                self._col_name_ram_usage, self._col_name_ram_used, self._col_name_disk_swap_usage, self._col_name_disk_swap_used,
                self._col_name_program_running
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            try:
                while True:
                    # Get system statistics
                    cpu_usage_per_core = self._get_cpu_usage_per_core()
                    overall_cpu_usage = self._get_overall_cpu_usage()
                    ram_percent, ram_used = self._get_ram_usage()
                    disk_percent, disk_used = self._get_disk_usage()
                    timestamp = time.time() - self._start_time

                    # Create a dictionary for the row data
                    row_data = {
                        self._col_name_timestamp: timestamp,
                        self._col_name_cpu_usage: overall_cpu_usage,
                        self._col_name_ram_usage: ram_percent,
                        self._col_name_ram_used: ram_used,
                        self._col_name_disk_swap_usage: disk_percent,
                        self._col_name_disk_swap_used: disk_used,
                        self._col_name_program_running: SystemStatsCollector.is_program_running(self._file_profiled)
                    }

                    # Populate CPU core data dynamically based on the number of cores
                    for idx, cpu_core in enumerate(cpu_usage_per_core):
                        row_data[self._col_name_cpu_cores[idx]] = cpu_core

                    # Write the row to the CSV file
                    writer.writerow(row_data)

                    print(f"Execution time: {timestamp:.3f} seconds")

            except KeyboardInterrupt:
                pass

            finally:
                end_time = time.time()
                total_execution_time = end_time - self._start_time
                print(f"\nTotal Execution Time: {total_execution_time:.2f} seconds")


# -----------------
# Main
# -----------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect system stats and write them to a CSV file.")
    parser.add_argument("--csv_file", default="system_stats.csv", help="Path to the CSV file for storing system stats.")
    parser.add_argument("--profiled_file", default="test_script", help="Name of the program to profile.")

    args = parser.parse_args()

    stats_collector = SystemStatsCollector(args.csv_file, args.profiled_file)
    stats_collector.measure_and_write_stats_to_csv()
