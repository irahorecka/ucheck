"""
ucheck.utils
~~~~~~~~~~~~

Provides utility class(es) and function(s) for ucheck.ucheck.
"""


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
