"""
This module contains basic UI tests using Playwright.
Their purpose is to show how to use the pytest framework by example.

By default playwright runs browser in headless mode, to make it headed we need to pass --headed
To see the browser window, we can pass --slowmo <time_in-miliSeconds>
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import re

from playwright.sync_api import Page, expect


# --------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------

@pytest.mark.login
def test_login(page: Page):
    # Arrange
    page.goto('https://demo.applitools.com/')

    # Act
    page.locator('id=username').fill('demoUser')
    page.locator('id=password').fill('demoPassword')
    page.locator('id=log-in').click()

    # Assert
    expect(page.locator('div.logo-w')).to_be_visible()
    expect(page.locator('ul.main-menu')).to_be_visible()
    expect(page.get_by_text('Add Account')).to_be_visible()
    expect(page.get_by_text('Make Payment')).to_be_visible()
    expect(page.get_by_text('View Statement')).to_be_visible()
    expect(page.get_by_text('Request Increase')).to_be_visible()
    expect(page.get_by_text('Pay Now')).to_be_visible()

    warning_msg = re.compile(r'Your nearest branch closes in:( \d+[hms])+')
    expect(page.locator('id=time')).to_have_text(warning_msg)

    acceptable_statuses = ['Complete', 'Pending', 'Declined']
    actual_statuses = page.locator('span.status-pill + span').all_text_contents()
    for status in actual_statuses:
        assert status in acceptable_statuses
