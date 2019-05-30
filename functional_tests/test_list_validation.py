from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_item(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_item_text:invalid'
            )
        )

        self.get_item_input_box().send_keys('Buy peacock feathers')

        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_item_text:valid'
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy peacock feathers')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_item_text:invalid'
            )
        )

        self.get_item_input_box().send_keys('Buy milk')

        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_item_text:valid'
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy peacock feathers')
        self.wait_for_row_in_list_table('2. Buy milk')

    def test_can_not_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy milk')

        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'duplicate item'
        ))
