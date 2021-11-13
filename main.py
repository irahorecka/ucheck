import os
import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

from ucheck import UCheck

if __name__ == "__main__":
    utorid_login = os.environ.get("UTORID_USER")
    utorid_password = os.environ.get("UTORID_PASS")
    with UCheck(Chrome, Service, "/opt/WebDriver/bin/chromedriver") as ucheck:
        ucheck.complete_ucheck(utorid_login, utorid_password)
        time.sleep(5)
