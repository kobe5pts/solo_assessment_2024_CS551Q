import urllib
from urllib.parse import urljoin
from behave import *
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('the user is on the login page')
def step_impl(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/login/')
    context.browser.get(open_url)

@when('the user enters valid credentials')
def step_impl(context):
    try:
        # Wait for the email text field to be present on the page
        email_textfield = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        # Send keys to the email text field
        email_textfield.send_keys('codio@codio.com')

        # Wait for the password text field to be present on the page
        password_textfield = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        # Send keys to the password text field
        password_textfield.send_keys('kobe5pts')

        # Wait for the submit button to be present on the page
        submit_button = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.NAME, 'submit'))
        )
        # Click the submit button
        submit_button.click()
    except Exception as e:
        # Handle exceptions
        print("An error occurred:", e)    

@then('the user should be redirected to the dashboard')
def step_impl(context):
    page_source = context.browser.page_source
    print("Page source:", page_source)  # Debug output
    assert page_source, "Dashboard not found in page source"
    print("Redirected to dashboard successfully")  # Debug output
    context.browser.quit()
