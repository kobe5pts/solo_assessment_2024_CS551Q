Feature: Product Purchase

  Scenario: Add product to cart and proceed to checkout
    Given the user is logged into the application
    When the user adds a product to the cart and proceeds to checkout
    Then the user should be directed to the checkout page