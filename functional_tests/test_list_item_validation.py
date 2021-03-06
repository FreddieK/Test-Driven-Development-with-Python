from .base import FunctionalTest
from unittest import skip
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Browser doesn't comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_item(self):
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')

        # Trying to add duplicate
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Error message shown
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            DUPLICATE_ITEM_ERROR
        ))

    @skip
    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)

        self.add_list_item('Banter too thick')

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element()
                .is_displayed()
        ))

        self.get_item_input_box().send_keys('a')

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element()
                .is_displayed()
        ))

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
