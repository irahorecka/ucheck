from pathlib import Path

import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from ucheck.exceptions import InvalidUTORidLogin
from ucheck.utils import ElementLocator

with open(Path(__file__).absolute().parent / "config.yaml", "r", encoding="utf-8") as config:
    CONSTANTS = yaml.safe_load(config)["constants"]
ELEMENTS_ABSXPATH = CONSTANTS["elements"]["abs-xpath"]
KEYWORDS = CONSTANTS["keywords"]


class UCheck:
    """
    Handles the UTORid login and the filling and submission of the COVID-19 UCheck form.

    Arguments:
    webdriver - Selenium webdriver class
    webdriver_service - Child webdriver service class of webdriver
    driver_path - Path to the webdriver executable
    """

    def __init__(self, webdriver, webdriver_service, driver_path):
        self.driver = webdriver(service=webdriver_service(driver_path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.close()

    def complete_ucheck(self, utorid_login, utorid_password):
        """Simple public method to 1) Log into portal (using UTORid credentials),
        2) Complete the UCheck form **to allow user to phsyically come on campus**,
        3) Submit the UCheck form."""
        self._login_to_portal(utorid_login, utorid_password)
        self._complete_ucheck_form()
        self._submit_ucheck_form()

    def _login_to_portal(self, utorid_login, utorid_password):
        """Log into UCheck portal using UTORid credentials. Raise exception if credentials
        are invalid."""
        self.driver.get(CONSTANTS["ucheck-url"])
        # Fill login credentials
        login = self.driver.find_element(By.XPATH, ELEMENTS_ABSXPATH["input"]["utorid-login"])
        login.clear()
        login.send_keys(utorid_login)
        # Fill password credentials
        password = self.driver.find_element(By.XPATH, ELEMENTS_ABSXPATH["input"]["utorid-password"])
        password.clear()
        password.send_keys(utorid_password)
        # Log in
        login.send_keys(Keys.RETURN)
        # Validate login
        self._validate_login_to_portal()

    def _validate_login_to_portal(self):
        """Validates successful login via UTORid portal."""
        try:
            self.driver.find_element(
                By.XPATH,
                f"{ELEMENTS_ABSXPATH['p']['invalid-utorid-login']}[contains(text(), '{KEYWORDS['contains']['invalid-utorid-login']}')]",
            )
            raise InvalidUTORidLogin(
                "Invalid UTORid credentials. Please verify your UTORid login and password and try again."
            )
        except NoSuchElementException:
            pass

    def _complete_ucheck_form(self):
        """Clicks appropriate radio buttons to allow user to successfully complete the
        UCheck form."""
        ucheck_form_abs_xpaths = ELEMENTS_ABSXPATH["input"]["ucheck-form"]
        for abs_expath in ucheck_form_abs_xpaths:
            self._click_radio_button(abs_expath)

    def _click_radio_button(self, abs_xpath):
        """Clicks radio button as provided by the absolute XPath."""
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ElementLocator((By.XPATH, abs_xpath)))
        self.driver.execute_script("arguments[0].click();", element)

    def _submit_ucheck_form(self):
        """Submits completed UCheck form."""
        submit = self.driver.find_element(
            By.XPATH, ELEMENTS_ABSXPATH["button"]["ucheck-form-submit"]
        )
        submit.send_keys(Keys.RETURN)
