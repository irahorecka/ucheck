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

    def complete_ucheck(self, utorid_user, utorid_pass):
        """Public method that 1) Logs into UCheck portal using UTORid credentials,
        2) Completes the UCheck form to allow user to physically come onsite to campus,
        3) Submits the completed UCheck form."""
        self._login_to_portal(utorid_user, utorid_pass)
        self._complete_ucheck_form()
        self._submit_ucheck_form()

    def _login_to_portal(self, utorid_user, utorid_pass):
        """Logs into UCheck portal using UTORid credentials. Raise exception if credentials
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
        try:
            self.driver.find_element(
                By.XPATH,
                f"{ELEMENTS_ABSXPATH['p']['invalid-utorid-user']}[contains(text(), '{KEYWORDS['contains']['invalid-utorid-user']}')]",
            )
            raise InvalidUTORidLogin(
                "Invalid UTORid credentials. Please verify your UTORid login and password then try again."
            )
        except NoSuchElementException:
            pass

    def _complete_ucheck_form(self):
        """Completes the UCheck form to allow user to physically come on campus."""
        ucheck_forms = ELEMENTS_ABSXPATH["input"]["ucheck-form"]
        for form in ucheck_forms:
            self._click_radio_button(form)

    def _click_radio_button(self, form_xpath):
        """Clicks a form's radio button as provided by the absolute XPath."""
        wait = WebDriverWait(self.driver, 10)
        radio_button = wait.until(ElementLocator((By.XPATH, form_xpath)))
        self.driver.execute_script("arguments[0].click();", radio_button)

    def _submit_ucheck_form(self):
        """Submits the completed UCheck form."""
        submit = self.driver.find_element(
            By.XPATH, ELEMENTS_ABSXPATH["button"]["ucheck-form-submit"]
        )
        submit.send_keys(Keys.RETURN)
