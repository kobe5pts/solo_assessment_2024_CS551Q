Feature: Product Search Functionality

  Scenario: Verify search functionality
    Given the user is on the products page
    When the user enters a search query
    Then the application should display relevant products matching the search query