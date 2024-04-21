import urllib
from urllib.parse import urljoin
from behave import *
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('the user is on the products page')
def step_impl(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/store/')
    context.browser.get(open_url)

@when('the user enters a search query')
def step_impl(context):
    try:
        # Wait for the search text field to be present on the page
        search_textfield = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search"]'))
        )
        # Send keys to the search text field
        search_textfield.send_keys('blackberry q5')

        # Wait for the submit button to be present on the page
        submit_button = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'submit'))
        )
        # Click the submit button
        submit_button.click()
    except Exception as e:
        # Handle exceptions
        print("An error occurred:", e)


@then('the application should display relevant products matching the search query')
def step_impl(context):
    # Validate that the search results are relevant
    results = context.browser.page_source    
    print("Page source:", results)  # Debug output
    assert "Items found" in results
    context.browser.quit()
