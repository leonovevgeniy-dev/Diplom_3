from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def click(self, locator, timeout=15):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable(locator)).click()
    
    def get_text(self, locator, timeout=15):
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.visibility_of_element_located(locator))
        return element.text
    
    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, text, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
    
    def wait_for_url_to_be(self, url, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))