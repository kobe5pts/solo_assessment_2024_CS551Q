import urllib
from urllib.parse import urljoin
from behave import *
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse

@given('the user is logged into the application')
def step_impl(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url,'/login/')
    context.browser.get(open_url)
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

@when('the user adds a product to the cart and proceeds to checkout')
def step_impl(context):
    category_slug='android'
    product_slug = '10or-g2-6gb-ram-64gb-charcoal-black'
    product_detail_url = reverse('product_detail', kwargs={'category__slug': category_slug, 'product_slug': product_slug})
    context.browser.get(product_detail_url)
    add_to_cart_button = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.ID, 'add-to-cart-button'))
    )
    add_to_cart_button.click()
    proceed_to_checkout_button = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.ID, 'proceed-to-checkout-button'))
    )
    proceed_to_checkout_button.click()

@then('the user should be directed to the checkout page')
def step_impl(context):
    expected_url = reverse('checkout')  # Assuming 'checkout' is the name of the checkout view URL
    assert context.browser.current_url == expected_url, "User not directed to the checkout page"
    context.browser.quit()