# import allure
# from playwright.async_api import Page
# from conf.conftest import playwright_context
#
#
# @allure.feature("UI Automation")
# @allure.parent_suite("JazzX UI Automation")
# @allure.suite("Sanity Test Cases")
# @allure.sub_suite("Postman APIs")
# class TestDemoUIs():
#
#     @allure.title("Test case to perform UI operation")
#     @allure.severity(allure.severity_level.NORMAL)
#     async def test_001(self, playwright_context):
#         # playwright_context: BrowserContext
#         page: Page = await playwright_context.new_page()
#         await page.goto('https://www.google.com')
#         t1: str = await page.title()
#
#         print('Done')
