import inspect
import json

import allure
from requests import Response

from common.rest_client import RestClient
from conf.conftest import api_setup_teardown


@allure.feature("API Automation")
@allure.parent_suite("JazzX API Automation")
@allure.suite("Sanity Test Cases")
@allure.sub_suite("Postman APIs")
class TestDemoAPIs():

    @allure.title("Test case to perform GET operation using Postman APIs")
    @allure.severity(allure.severity_level.NORMAL)
    def test_002(self, api_setup_teardown):
        env_under_test, config_data, user_asserts, logger = api_setup_teardown
        test_case_name = inspect.currentframe().f_code.co_name

        logger.info(f"Test under execution : {test_case_name}")
        base_url = config_data['base_url']

        # Initialize headers. Can be moved to separate file later.
        headers = {
            'x-api-key': config_data['api_key'],
            'Content-Type': 'application/json',
            'User-Agent': 'my-app/0.0.1'
        }

        # Request preparation.
        rest_client = RestClient(logger)
        rest_client.set_base_url(base_url)
        rest_client.set_request_header(headers=headers)
        rest_client.set_end_point('/workspaces?')

        # Send Request.
        response: Response = rest_client.get_request()

        # User asserts.
        user_asserts.assert_actual_expected_to_be_equal(expected_value=201, actual_value=response.status_code,
                                                        log_info='Actual and expected should match')

    @allure.title("Test case to perform POST operation using Postman APIs")
    @allure.severity(allure.severity_level.NORMAL)
    def test_003(self, api_setup_teardown):
        env_under_test, config_data, user_asserts, logger = api_setup_teardown
        test_case_name = inspect.currentframe().f_code.co_name

        logger.info(f"Test under execution : {test_case_name}")
        base_url = config_data['base_url']

        # Initialize headers. Can be moved to separate file later.
        headers = {
            'x-api-key': config_data['api_key'],
            'Content-Type': 'application/json',
            'User-Agent': 'my-app/0.0.1'
        }

        # Prepare request data. Can be moved to separate request file later.
        request_data = {
            "workspace": {
                "name": "created_from_python_framework",
                "type": "personal",
                "description": "created for testing purpose"
            }
        }

        # Request preparation.
        rest_client = RestClient(logger)
        rest_client.set_base_url(base_url)
        rest_client.set_request_header(headers=headers)
        rest_client.set_end_point('/workspaces?')
        rest_client.set_api_request_data(request_data)

        # Send post request.
        response: Response = rest_client.post_request()
        response_body: dict = response.json()

        workspace_name = response_body['workspace']['name']
        workspace_id = response_body['workspace']['id']

        logger.info(f'Workspace name : {workspace_name}')
        logger.info(f'Workspace id : {workspace_id}')

        # User asserts.
        request_data_dict = json.loads(rest_client.get_api_request_data())
        user_asserts.assert_actual_expected_to_be_equal(expected_value=200, actual_value=response.status_code,
                                                        log_info='Actual and expected should match')

        user_asserts.assert_actual_expected_to_be_equal(expected_value=request_data_dict['workspace']['name'],
                                                        actual_value=workspace_name)

    ''' 
     In this use case we will first create a new workspace.
     We will do assert with initial name for workspace
     By using put method, we will update/replace the Workspace
     We will validate new workspace name after PUT
    '''
    @allure.title("Test case to perform PUT operation using Postman APIs")
    @allure.severity(allure.severity_level.NORMAL)
    def test_004(self, api_setup_teardown):
        env_under_test, config_data, user_asserts, logger = api_setup_teardown
        test_case_name = inspect.currentframe().f_code.co_name

        logger.info(f"Test under execution : {test_case_name}")
        base_url = config_data['base_url']

        # create new workspace
        # Initialize headers. Can be moved to separate file later.
        headers = {
            'x-api-key': config_data['api_key'],
            'Content-Type': 'application/json',
            'User-Agent': 'my-app/0.0.1'
        }

        # Prepare request data. Can be moved to separate request file later.
        request_data = {
            "workspace": {
                "name": "created_from_python_framework",
                "type": "personal",
                "description": "created for testing purpose"
            }
        }

        # Request preparation.
        rest_client = RestClient(logger)
        rest_client.set_base_url(base_url)
        rest_client.set_request_header(headers=headers)
        rest_client.set_end_point('/workspaces?')
        rest_client.set_api_request_data(request_data)

        # Send post request.
        response: Response = rest_client.post_request()
        response_body: dict = response.json()
        initial_workspace_name = response_body['workspace']['name']
        initial_workspace_id = response_body['workspace']['id']

        logger.info(f'Initial workspace name: {initial_workspace_name}')
        logger.info(f'Initial workspace id : {initial_workspace_id}')

        # User asserts - POST Request
        request_data_dict = json.loads(rest_client.get_api_request_data())
        user_asserts.assert_actual_expected_to_be_equal(expected_value=200, actual_value=response.status_code,
                                                        log_info='Actual and expected should match')

        user_asserts.assert_actual_expected_to_be_equal(expected_value=request_data_dict['workspace']['name'],
                                                        actual_value=initial_workspace_name)

        # PUT request.
        # Put request data preparation
        request_data_put = {
            "workspace": {
                "id": initial_workspace_id,
                "name": "new_name",
                "type": "personal",
                "visibility": "personal",
                "createdBy": "6134147",
            }
        }

        # PUT Request preparation.
        rest_client_put = RestClient(logger)
        rest_client_put.set_base_url(base_url)
        rest_client_put.set_request_header(headers=headers)
        rest_client_put.set_end_point(f'/workspaces/{initial_workspace_id}')
        rest_client_put.set_api_request_data(request_data_put)

        # Send PUT request.
        response_put: Response = rest_client_put.put_request()

        response_body: dict = response_put.json()
        workspace_name_after_put = response_body['workspace']['name']
        workspace_id_after_put = response_body['workspace']['id']

        logger.info(f'Workspace name after put : {workspace_name_after_put}')
        logger.info(f'Workspace id after put: {workspace_id_after_put}')

        # User asserts - PUT Request
        request_data_dict_put = json.loads(rest_client_put.get_api_request_data())
        user_asserts.assert_actual_expected_to_be_equal(expected_value=200, actual_value=response_put.status_code,
                                                        log_info='Actual and expected should match')

        user_asserts.assert_actual_expected_to_be_equal(expected_value=request_data_dict_put['workspace']['name'],
                                                        actual_value=workspace_name_after_put)
