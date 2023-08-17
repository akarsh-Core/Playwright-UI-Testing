import pytest
import re

from playwright.sync_api import Page, expect


@pytest.mark.loadPage
def test_page_loading(page: Page):
    # Arrange
    page.goto('https://demo.borland.com/gmoajax/catalog.php')

    # Assert
    expect(page.locator('//*[@id="Layout Options"]/h3')).to_be_visible()
    # expect(page.locator('id=discalimer-footer')).to_be_visible()
    expect(page.get_by_text('Disclaimer')).to_be_visible()
    cart_items = page.locator('id=cart-qty').text_content().split()[0]
    assert int(cart_items) == 0


@pytest.mark.addToCart
def test_added_to_cart(page: Page):
    page.goto('https://demo.borland.com/gmoajax/catalog.php')

    # verify cart is empty when we load the page
    cart_items = page.locator('id=cart-qty').text_content().split()[0]
    assert int(cart_items) == 0

    # add 1 item to cart -
    xpath_expression_women_boots = "//html/body/div/div[2]/div/ul/li[2]/button"
    page.locator(xpath_expression_women_boots).click()

    # as it is a demo page, it is taking some time to be updated
    page.wait_for_timeout(3000)

    # verify cart has 1 item -
    cart_items = page.locator('id=cart-qty').text_content().split()[0]
    assert int(cart_items) == 1

    # add another item to cart -
    xpath_expression_led_torch = "//html/body/div/div[2]/div/ul/li[8]/button"
    page.locator(xpath_expression_led_torch).click()

    page.wait_for_timeout(3000)

    # verify cart has 2 items -
    cart_items = page.locator('id=cart-qty').text_content().split()[0]
    assert int(cart_items) == 2


@pytest.mark.checkout
def test_confirm_cart_redirection(page: Page):
    page.goto('https://demo.borland.com/gmoajax/catalog.php')

    # verify cart is empty when we load the page
    cart_items = page.locator('id=cart-qty').text_content().split()[0]
    assert int(cart_items) == 0

    # add 1 item to cart -
    xpath_expression_tent = "//html/body/div/div[2]/div/ul/li[6]/button"
    page.locator(xpath_expression_tent).click()

    page.wait_for_timeout(3000)

    # verify cart has 1 item -
    cart_items = page.locator('id=cart-qty').text_content().split()[0]
    assert int(cart_items) == 1

    # click on cart button to go to cart page
    xpath_expression_cart = '//html/body/div/div[1]/a[2]/img'
    cart_button = page.locator(xpath_expression_cart)
    cart_button.click()

    # page.wait_for_timeout(3000)
    page.wait_for_selector('id=Modal Header')

    confirm_button = page.locator('id=modalBtn Confirm')
    confirm_button.click()

    # after clicking on confirm, wait for payment page
    page.wait_for_url('https://demo.borland.com/gmoajax/payment_details.php')

    found_title = page.locator('id=mainTitle')
    print(found_title.text_content())
