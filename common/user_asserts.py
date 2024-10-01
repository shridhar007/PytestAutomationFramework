from logging import Logger

import allure


class UserAsserts():

    def __init__(self, logger: Logger):
        self.logger = logger

    @allure.step("Hard Assert - Actual {1} and expected {2} to be equal")
    def assert_actual_expected_to_be_equal(self, expected_value, actual_value, log_info: str = None) -> None:
        self.logger.info(log_info)
        self.logger.info(f'Expected value - {expected_value} : Actual value - {actual_value}')
        assert actual_value == expected_value

    @allure.step("Hard Assert - Actual {1} and expected {2} are not equal")
    def assert_actual_expected_are_not_equal(self, expected_value, actual_value, log_info: str = None) -> None:
        self.logger.info(log_info)
        self.logger.info(f'Expected value - {expected_value} : Actual value - {actual_value}')
        assert actual_value != expected_value

