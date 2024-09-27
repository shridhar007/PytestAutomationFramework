import json
from datetime import time
from logging import Logger
from platform import system

import allure
import pytest
import requests
from requests import Response


class RestClient:
    # def __init__(self, base_url, headers, logger):
    #     self.http_session = requests.Session()
    #     self.http_session.verify = True
    #
    #     self.base_url = base_url
    #     self.http_session.headers = headers
    #     self.logger = logger
    #
    #     logger.info(f"Base url is : {self.base_url}")
    #     self.success_status_code = (200, 201, 202, 204)

    def __init__(self, logger: Logger):
        self._https_session = requests.Session()
        self._https_session.verify = True
        self.logger: Logger = logger

        self._base_url = None
        self._https_session.headers = None
        self._end_point = None
        self._params = None
        self._request_data = None
        self._request_param = None

        # self.logger.info(f"Base url is : {self._base_url}")
        self.success_status_code = (200, 201, 202, 204)

    @allure.step("Get Base URL")
    def get_base_url(self) -> str:
        if self._base_url is None:
            self.logger.exception(f'Base URL is not set. Terminating test execution...')
            return ''
        return self._base_url

    @allure.step("Set Base URL")
    def set_base_url(self, base_url: str):
        self._base_url = base_url

    @allure.step("Set request headers")
    def set_request_header(self, headers):
        self._https_session = requests.Session()
        self._https_session.headers = headers

    @allure.step("Get request headers")
    def get_request_headers(self):
        return self._https_session.headers

    @allure.step("Set api end point")
    def set_end_point(self, end_point: str) -> None:
        self._end_point = end_point

    @allure.step("Get api end point")
    def get_api_end_point(self) -> str:
        if self._end_point is None:
            self.logger.exception(f'API end point is not set. Terminating test execution...')
            return ''
        return self._end_point

    @allure.step('Set API request data')
    def set_api_request_data(self, req_data: dict) -> None:
        req_data_json_format = json.dumps(req_data)
        self._request_data = req_data_json_format

    @allure.step('Get API request data')
    def get_api_request_data(self) -> str:
        return self._request_data

    @allure.step('Set API request parameters')
    def set_api_request_param(self, req_param: str) -> None:
        self._request_param = req_param

    @allure.step('Get API request parameters')
    def get_api_request_param(self) -> str:
        return self._request_param


    @allure.step("Perform GET request")
    def get_request(self) -> Response:
        if self._end_point is None:
            request_url = self._base_url
        else:
            request_url = self._base_url + self._end_point

        try:
            request_data = json.dumps(self._request_data)
            self.logger.info(f"Initializing GET rest call from {request_url}")

            response: Response = self._https_session.get(request_url, params=self._request_param,
                                                         headers=self._https_session.headers,
                                                         data=request_data, verify=True)

            if response.status_code in self.success_status_code:
                self.logger.info("GET request is Successful.....")
            else:
                self.logger.error(f"GET Request failed....!!!")
                self.logger.error(f"Response Error Message: {self.parse_response(response)}")

            return response

        except Exception as exception:
            self.logger.info(f"GET request failed...")
            self.logger.exception(f"Exception occurred : {exception}")
            pytest.fail(f'Test case failed due to exception {exception}')

    @allure.step("Perform POST request")
    def post_request(self):
        if self._end_point is None:
            request_url = self._base_url
        else:
            request_url = self._base_url + self._end_point

        try:
            # request_data = json.dumps(self._request_data)
            self.logger.info(f"Initializing GET rest call from {request_url}")

            response: Response = self._https_session.post(request_url, params=self._request_param,
                                                          headers=self._https_session.headers,
                                                          data=self._request_data, verify=True)

            if response.status_code in self.success_status_code:
                self.logger.info("POST request is Successful.....")
            else:
                self.logger.error(f"POST Request failed....!!!")
                self.logger.error(f"Response Error Message: {self.parse_response(response)}")
                pytest.fail(f'Test case failed with response code {response.status_code}')

            return response

        except Exception as exception:
            self.logger.info(f"POST request failed...")
            self.logger.exception(f"Exception occurred : {exception}")
            pytest.fail(f'Test case failed due to exception {exception}')

    @allure.step("Perform PUT request")
    def put_request(self):
        if self._end_point is None:
            request_url = self._base_url
        else:
            request_url = self._base_url + self._end_point

        try:
            self.logger.info(f"Initializing GET rest call from {request_url}")

            response: Response = self._https_session.put(request_url, params=self._request_param,
                                                          headers=self._https_session.headers,
                                                          data=self._request_data, verify=True)

            if response.status_code in self.success_status_code:
                self.logger.info("PUT request is Successful.....")
            else:
                self.logger.error(f"PUT Request failed....!!!")
                self.logger.error(f"Response Error Message: {self.parse_response(response)}")
                pytest.fail(f'Test case failed with response code {response.status_code}')

            return response

        except Exception as exception:
            self.logger.info(f"PUT request failed...")
            self.logger.exception(f"Exception occurred : {exception}")
            pytest.fail(f'Test case failed due to exception {exception}')


    def delete_request(self, end_point, data=None, headers=None, json_data_fmt=None, params=None,
                       fmt="json", response_with_status_code=False, auto_save=False):
        """
        This method is to send delete request
        :param end_point (str): API endpoint/URL
        :param data (dict): Body of a request
        :param headers (dict): Parameters for a request
        :param json_data_fmt (bool): True if data should be in json else False
        :param params: Used for response type json or raw
        :param fmt:
        :param response_with_status_coode (bool): True if Status code os required else False
        :param auto_save (bool) : saves response into json file if True else False
        :return: Response of the request

        """
        request_url = self.base_url + end_point

        self.logger.info(f"Request url is : {request_url}")
        if json_data_fmt:
            data = json.dumps(data)
        try:
            self.logger.info(f"Initializing DELETE REST call from {request_url}")
            delete_response = self.http_session.delete(request_url, params=params, headers=headers, data=data,
                                                       verify=True)
            response_data = self.parse_response(delete_response)

            self.logger.info(f"DELETE Response : {self.parse_response(delete_response)}")
            self.logger.info(f"DELETE request Status code : {delete_response.status_code}")

            if delete_response.status_code in self.success_status_code:
                self.logger.info(f"DELETE request is successful....")
                # if auto_save:
                #     save_json_to_file(response_data)
                if fmt == "raw":
                    return delete_response
                if response_with_status_code:
                    return self.parse_response(delete_response), delete_response.status_code
                return self.parse_response(delete_response)
            else:
                self.logger.error(f"PUT request Failed...!!!")
                self.logger.error(f"Response Error Message: {self.parse_response(delete_response)}")
                return self.parse_response(delete_response), delete_response.status_code

        except Exception as exc:
            self.logger.info("DELETE request is failed...!!!")
            self.logger.exception(f"Exception occurred : {exc}")

    def parse_response(self, response):
        """
        This method is to parse a response from the API.
        :param response: request response
        :return: parsed response based on expected format
        """
        try:
            # Check if the response is a requests.Response object
            if hasattr(response, 'headers'):
                content_type = response.headers.get('Content-Type')
                # Handle JSON responses
                if content_type in ['application/json', 'application/json; charset=utf-8']:
                    self.logger.info(f"Response JSON : {response.text}")
                    try:
                        return response.json()
                    except ValueError:
                        self.logger.error("Response content is not valid JSON.")
                        return None
                # Handle non-JSON responses (text, HTML, etc.)
                # elif response.text:
                #     self.logger.info(f"Response Text : {response.text}")
                #     return response.text

                else:
                    # For DELETE requests with no response content
                    if response.request.method.upper() == 'DELETE' and not response.content:
                        self.logger.info("DELETE request sent successfully, no response content returned.")
                        return None

                    self.logger.error("Unknown content type or empty response.")
                    return None

            # If response is directly passed (like list, str, tuple)
            elif isinstance(response, (list, str, tuple, dict)):
                return response

            else:
                self.logger.error("Unexpected response type encountered.")
                return None

        except Exception as exc:
            self.logger.exception(f"Failed to parse response: {str(exc)}")
            time.sleep(5)
            raise exc
