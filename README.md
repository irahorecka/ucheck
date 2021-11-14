# ucheck

Automate UCheck COVID-19 self-assessments form submission.

## Disclaimer

* ucheck automatically completes the University of Tornto's UCheck COVID-19 self-assessment form as follows:
    * **YES**: "Do any of the following statements apply to you? - I am fully vaccinated against COVID-19."
    * **NO**: "Are you currently experiencing any of these symptoms? - Fever and/or chills (Temperature of 37.8 degrees Celsius/100 degrees Fahrenheit or higher)."
    * **NO**: "Is anyone you live with currently experiencing any new COVID-19 symptoms and/or waiting for test results after experiencing symptoms?"
    * **NO**: "In the last 14 days, have you travelled outside of Canada and been told to quarantine (per the federal quarantine requirements)?"
    * **NO**: "Has a doctor, health care provider, or public health unit told you that you should currently be isolating (staying at home)?"
    * **NO**: "In the last 10 days, have you been identified as a "close contact" of someone who currently has COVID-19?"
    * **NO**: "In the last 14 days, have you received a COVID Alert exposure notification on your cell phone?"
    * **NO**: "In the last 10 days, have you tested positive on a rapid antigen test or home-based self-testing kit?"
* If you do not satisfy these questions as listed, DO NOT use this library to complete your UCheck form. If you are interested in making these choices customizable, please raise an issue using the [issues tracker](https://github.com/irahorecka/ucheck/issues).

## Installation

```bash
$ pip install ucheck
```

## Requirements and setup

This library uses [Selenium](https://selenium-python.readthedocs.io/) to complete the UCheck form. If you are new to Selenium, it takes ~5 minutes to download and set up your browser driver. View [how to download and configure a browser driver](https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/). If you are on a Mac, [this Stackoverflow article](https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de) may help to allow your OS to use Selenium without running into OS-related security issues.

## ucheck is simple to use

```python
import os
import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

from ucheck import UCheck

if __name__ == "__main__":
    # E.g., Save UTORid login and password as environment variables.
    utorid_login = os.environ["UTORID_USER"]
    utorid_password = os.environ["UTORID_PASS"]
    with UCheck(Chrome, Service, driver_path="/opt/WebDriver/bin/chromedriver") as ucheck:
        ucheck.complete_ucheck(utorid_login, utorid_password)
        # Briefly keep browser window open before closing.
        time.sleep(5)
```

## Exceptions

Valid UTORid credentials are required to use ucheck.

```python
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

from ucheck import UCheck
from ucheck.exceptions import InvalidUTORidLogin

if __name__ == "__main__":
    # Set invalid user login credentials.
    utorid_login = "invalid-login"
    utorid_password = os.environ["UTORID_PASS"]
    with UCheck(Chrome, Service, "/opt/WebDriver/bin/chromedriver") as ucheck:
        try:
            ucheck.complete_ucheck(utorid_login, utorid_password)
        except InvalidUTORidLogin as e:
            print(e)
```

## Contribute

- [Issue Tracker](https://github.com/irahorecka/ucheck/issues)
- [Source Code](https://github.com/irahorecka/ucheck/tree/master/ucheck)

## Support

If you are having issues or would like to propose a new feature, please use the [issues tracker](https://github.com/irahorecka/ucheck/issues).

## License

The project is licensed under the MIT license.
