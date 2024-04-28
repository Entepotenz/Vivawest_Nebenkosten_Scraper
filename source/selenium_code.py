import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def run_selenium_init(url_to_scrape: str, headless: bool = True):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1280,720")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")  # Not used
    driver = webdriver.Chrome(options=options)

    driver.get(url_to_scrape)
    return driver


def run_selenium_login(driver, username: str, password: str):
    max_wait_time_in_seconds = 5  # seconds
    time.sleep(5)
    try:
        WebDriverWait(driver, max_wait_time_in_seconds).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "usercentrics-root")
            )
        )
        driver.execute_script(
            """
            return document.querySelector('div#usercentrics-root')\
            .shadowRoot\
            .querySelector('button[data-testid="uc-accept-all-button"]')
            """
        ).click()
    except NoSuchElementException as exception:
        logging.warning(exception)

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-backdrop")
        )
    )

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located((By.ID, "login-username"))
    )
    driver.find_element(By.ID, "login-username").send_keys(username)
    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located((By.ID, "login-password"))
    )
    driver.find_element(By.ID, "login-password").send_keys(password)
    driver.find_element(By.ID, "loginForm").submit()

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-backdrop")
        )
    )


def run_selenium_logout(driver):
    max_wait_time_in_seconds = 5  # seconds
    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located((By.ID, "user-menu"))
    )
    driver.find_element(By.ID, "user-menu").click()

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(@class, 'dropdown-item') and contains(@class, 'logout')]",
            )
        )
    )
    driver.find_element(
        By.XPATH,
        "//a[contains(@class, 'dropdown-item') and contains(@class, 'logout')]",
    ).click()

    driver.close()
