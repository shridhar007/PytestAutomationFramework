import allure
from playwright.sync_api import Page, BrowserContext
from conf.conftest import playwright_page


@allure.feature("UI Automation")
@allure.parent_suite("Google Homepage Automation")
@allure.suite("Sanity Test Cases")
@allure.sub_suite("UI Automation")
class TestDemoUI():

    @allure.title("Test case to perform GET operation using Postman APIs")
    @allure.severity(allure.severity_level.NORMAL)
    def test_002_ui(self, playwright_page: Page):
        playwright_page.goto("https://www.google.com")
        t1 = playwright_page.title()
        print(t1)