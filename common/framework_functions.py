import configparser
from configparser import ConfigParser
from pathlib import Path

import cryptocode


class CommonFunctions:
    exec_config: ConfigParser = None

    @staticmethod
    def get_project_root_path():
        current_path: Path = Path.cwd()
        root_path: Path

        # check if current dir is root dir or not.
        if (current_path / '.github').exists() or (current_path / '.venv').exists() or (
                current_path / 'qa_tests').exists():
            return current_path

        for parent in current_path.parents:
            if (parent / '.github').exists() or (parent / '.venv').exists() or (parent / 'qa_tests').exists():
                root_path = parent

        if root_path.exists():
            return root_path
        else:
            raise Exception("Error in finding root path. Existing")

    @staticmethod
    def read_ini_file(file_name: str, root_dir: Path) -> None:
        api_test_config_file_path: Path = root_dir.joinpath('conf', file_name)

        if api_test_config_file_path.exists():
            config: ConfigParser = configparser.ConfigParser()
            config.read(api_test_config_file_path)
        else:
            raise Exception(f"Failed to read *.ini file at {api_test_config_file_path}. Exiting...")

        CommonFunctions.exec_config = config

    @staticmethod
    def decrypt_key(encoded_str: str, key: str) -> str:
        print(encoded_str)
        print(key)
        return cryptocode.decrypt(encoded_str, key)
