import json
from datetime import time
from logging import Logger
from typing import MutableMapping

import allure
import pytest
import requests
from requests import Response


class RestClient:

    def __init__(self, logger: Logger):
        self._https_session = requests.Session()
        self._https_session.verify = True
        self.logger: Logger = logger
        self.success_status_code = (200, 201, 202, 204)

        self._base_url = None
        self._https_session.headers = None
        self._end_point = None
        self._params = None
        self._request_data = None
        self._request_param = None

    @property
    @allure.step("Get Base URL")
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    @allure.step("Set Base URL as {1}")
    def base_url(self, value: str):
        self._base_url = value

    @property
    @allure.step("Get request headers")
    def request_headers(self) -> MutableMapping[str, str | bytes]:
        return self._https_session.headers

    @request_headers.setter
    @allure.step("Set request headers as {1}")
    def request_headers(self, value):
        self._https_session = requests.Session()
        self._https_session.headers = value

    @property
    @allure.step("Get api end point")
    def end_point(self) -> str:
        if self._end_point is None:
            self.logger.exception(f'API end point is not set. Terminating test execution...')
            return ''
        return self._end_point

    @end_point.setter
    @allure.step("Set api end point as {1}")
    def end_point(self, value):
        self._end_point = value

    @property
    @allure.step('Get API request data')
    def request_data(self) -> str:
        return self._request_data

    @request_data.setter
    @allure.step('Set API request data as {1}')
    def request_data(self, value):
        req_data_json_format = json.dumps(value)
        self._request_data = req_data_json_format

    @property
    @allure.step('Get API request parameters')
    def request_param(self) -> str:
        return self._request_param

    @request_param.setter
    @allure.step('Set API request parameters as {1}')
    def request_param(self, value):
        self._request_param = value

    def validate_end_point(self) -> str:
        if self._end_point is None:
            request_url = self.base_url
        else:
            request_url = self.base_url + self.end_point

        return request_url

    @allure.step('Perform {1} request')
    def execute_request(self, request_type: str) -> Response:
        request_url = self.validate_end_point()
        response: Response = None
        try:
            self.logger.info(f"Initializing {request_type} rest call from {request_url}")
            match request_type.upper():
                case 'GET':
                    response: Response = self._https_session.get(request_url, params=self._request_param,
                                                                 headers=self._https_session.headers,
                                                                 data=self._request_data, verify=True)
                case 'POST':
                    response: Response = self._https_session.post(request_url, params=self._request_param,
                                                                  headers=self._https_session.headers,
                                                                  data=self._request_data, verify=True)
                case 'PUT':
                    response: Response = self._https_session.put(request_url, params=self._request_param,
                                                                 headers=self._https_session.headers,
                                                                 data=self._request_data, verify=True)
                case 'PATCH':
                    response: Response = self._https_session.patch(request_url, params=self._request_param,
                                                                   headers=self._https_session.headers,
                                                                   data=self._request_data, verify=True)
                case 'DELETE':
                    response: Response = self._https_session.delete(request_url, params=self._request_param,
                                                                    headers=self._https_session.headers,
                                                                    data=self._request_data, verify=True)
                case _:
                    self.logger.info(f"Invalid request type : {request_type}")

            if response.status_code in self.success_status_code:
                self.logger.info(f"{request_type} request is Successful.....")
            else:
                self.logger.error(f"{request_type} Request failed....!!!")
                self.logger.error(f"Response Error Message: {self.parse_response(response)}")
                pytest.fail(f'Test case failed with response code {response.status_code}')

            return response

        except Exception as exception:
            self.logger.info(f"{request_type} request failed...")
            self.logger.exception(f"Exception occurred : {exception}")
            pytest.fail(f'Test case failed due to exception {exception}')

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


if __name__ == '__main__':
    rest_client: RestClient = RestClient()
