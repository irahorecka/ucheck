"""
ucheck.ucheck
~~~~~~~~~~~~~

Handles the interface with the University of Toronto's UCheck COVID-19
self-assessment form.
"""

from pathlib import Path

import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from ucheck.exceptions import InvalidUTORidLogin

with open(Path(__file__).resolve().parent / "config.yaml", "r", encoding="utf-8") as config:
    CONSTANTS = yaml.safe_load(config)["constants"]
ELEMENTS_ABSXPATH = CONSTANTS["elements"]["abs-xpath"]
KEYWORDS = CONSTANTS["keywords"]


class UCheck:
    """
    Handles the UTORid login and the filling and submission of the COVID-19 UCheck form.

    Arguments:
    driver - Selenium webdriver class
    driver_service - Webdriver service class of driver
    driver_path - Path to the webdriver executable (e.g. ChromeDriver)
    """

    def __init__(self, driver, driver_service, driver_path):
        self.driver = driver(service=driver_service(driver_path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.close()

    def complete_ucheck(self, utorid_user, utorid_pass):
        """Public method that 1) Logs into UCheck portal using UTORid credentials,
        2) Completes UCheck forms to allow user to physically come onsite to campus,
        3) Submits the completed UCheck."""
        self._login_to_portal(utorid_user, utorid_pass)
        self._complete_ucheck_forms()
        self._submit_ucheck()

    def _login_to_portal(self, utorid_user, utorid_pass):
        """Logs into UCheck portal using UTORid credentials. Raises exception if credentials
        are invalid."""
        self.driver.get(CONSTANTS["ucheck-url"])
        # Fill login credentials
        login = self.driver.find_element(By.XPATH, ELEMENTS_ABSXPATH["input"]["utorid-user"])
        login.clear()
        login.send_keys(utorid_user)
        # Fill password credentials
        password = self.driver.find_element(By.XPATH, ELEMENTS_ABSXPATH["input"]["utorid-pass"])
        password.clear()
        password.send_keys(utorid_pass)
        # Log in and validate login
        login.send_keys(Keys.RETURN)
        self._validate_login_to_portal()

    def _validate_login_to_portal(self):
        """Validates successful login via UTORid portal."""
        for invalid_login_type, invalid_login_keyword in [
            (k, v)
            for keyword in KEYWORDS["contains"]["invalid-utorid-login"]
            for (k, v) in keyword.items()
        ]:
            try:
                self.driver.find_element(
                    By.XPATH,
                    f"{ELEMENTS_ABSXPATH['p']['invalid-utorid-login']}[contains(text(), '{invalid_login_keyword}')]",
                )
                raise InvalidUTORidLogin(
                    f"Invalid UTORid credentials. Please verify your UTORid {invalid_login_type} then try again."
                )
            except NoSuchElementException:
                pass

    def _complete_ucheck_forms(self):
        """Completes UCheck forms to allow user to physically come onsite to campus."""
        ucheck_forms = ELEMENTS_ABSXPATH["input"]["ucheck-forms"]
        for form in ucheck_forms:
            self._click_radio_button(form)

    def _click_radio_button(self, form_xpath):
        """Clicks a form's radio button as provided by the absolute XPath."""
        wait = WebDriverWait(self.driver, 10)
        radio_button = wait.until(ElementLocator((By.XPATH, form_xpath)))
        self.driver.execute_script("arguments[0].click();", radio_button)

    def _submit_ucheck(self):
        """Submits the completed UCheck."""
        submit = self.driver.find_element(By.XPATH, ELEMENTS_ABSXPATH["button"]["ucheck-submit"])
        submit.send_keys(Keys.RETURN)


class ElementLocator:
    """
    An expectation for checking that an element has a particular locator (e.g., absolute XPath).

    Arguments:
    locator - used to find the element

    Returns:
    WebElement once it finds the locator
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.locator:
            return element
        return False
