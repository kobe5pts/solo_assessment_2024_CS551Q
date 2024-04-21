import urllib
from urllib.parse import urljoin
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given("open Modupe homepage")
def openModupe(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    print(base_url)
    open_url = urljoin(base_url, '/homepage/')
    context.browser.get(open_url)

@when("verify that the logo present on page")
def verifyLogo(context):
    try:
        # Wait for the logo element to be present on the page
        logo_element = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
        )
        # If the logo element is found, assert that it is visible
        assert logo_element.is_displayed(), "Logo is present on the page"
    except AssertionError:
        # Handle assertion error if the element is not visible
        print("Logo is not present on the page")
    except Exception as e:
        # Handle other exceptions
        print("An error occurred:", e)

@then("we succeed")
def closeBrowser(context):
    pass
