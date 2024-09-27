import datetime
import logging
import os
from logging import Logger, FileHandler
from pathlib import Path



def log_generator(test_case_source: str, root_dir: Path) -> Logger:
    current_time_stamp: datetime = datetime.datetime.now()
    current_date: str = f'{str(current_time_stamp.day)}-{str(current_time_stamp.month)}-{str(current_time_stamp.year)}'
    current_time: str = f'{str(current_time_stamp.hour)}_{str(current_time_stamp.minute)}_{str(current_time_stamp.second)}'

    # Create a folder for the current date inside the Logs directory
    log_directory: Path = root_dir.joinpath('logs')

    if test_case_source.upper() == "API":
        log_directory: Path = log_directory.joinpath("api")
    elif test_case_source.upper() == "UI":
        log_directory: Path = log_directory.joinpath("ui")
    elif test_case_source.upper() == "IAC":
        log_directory: Path = log_directory.joinpath("iac")

    date_folder_path: Path = os.path.join(log_directory, current_date)
    os.makedirs(date_folder_path, exist_ok=True)

    # Define the log file path with timestamp
    log_file_path: Path = os.path.join(date_folder_path, f"log_{current_time}.log")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure the logging
    logger: Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler: FileHandler = logging.FileHandler(log_file_path, mode="w")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    return logger


# Enhancement - Add method to automatically delete historical logs which are no longer required.