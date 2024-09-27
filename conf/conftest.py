import platform
from pathlib import Path
import pytest

from common.framework_functions import CommonFunctions
from common.logger import log_generator
from _pytest.fixtures import SubRequest

from common.user_asserts import UserAsserts


@pytest.fixture(scope='class', autouse=True)
def api_setup_teardown(request: SubRequest):
    root_dir: Path = CommonFunctions.get_project_root_path()
    logger = log_generator("API", root_dir)
    user_asserts = UserAsserts(logger)

    # Read api_test_config.ini
    CommonFunctions.read_ini_file('api_test_config.ini', root_dir)
    env_under_test = CommonFunctions.exec_config['RUN_CONFIG']['environment']

    logger.info(f'Starting test setup process...')
    logger.info(f'API tests are configured for {env_under_test} environment')
    logger.info(f'BaseURL : {CommonFunctions.exec_config[f'{env_under_test} ENV']['base_url']}')

    yield env_under_test, CommonFunctions.exec_config[f'{env_under_test} ENV'], user_asserts, logger

    # Clean up code here.
    allure_dir = root_dir.joinpath('logs', 'allure-results')
    # command: str = f'allure generate --clean --single-file "{allure_dir}"'
    # logger.info(f'Allure single file generation command : {command}')

    #Prepare Environment Variables for Allure Report.
    env_template_filename = 'environment.properties'
    env_template_file_path = root_dir.joinpath('conf',env_template_filename)

    if env_template_file_path.exists():
        # Read env_template file and update values. Save new file in allure-results dir.
        logger.info("Allure Report: Environment file exists")
        content:str
        with open(env_template_file_path, 'r') as file:
            content = file.read()
            os_name = platform.system()
            content = content.replace('%OS_VERSION%', os_name)
            content = content.replace('%ENV%', env_under_test)
            content = content.replace("%PROJECT%", "Jazz X")
            logger.info("Allure Report: Environment file template read successfully. ")

        with open(allure_dir.joinpath('environment.properties'), 'w') as file:
            file.write(content)
            logger.info("Allure Report: Environment file template saved successfully. ")

    else:
        logger.info("Allure Report: Environment file do not exists")

@pytest.fixture(scope='class', autouse=True)
def setup_playwright_context():
    logger = log_generator("UI")
    pass
