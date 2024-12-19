import logging
import re
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

max_wait_time_in_seconds = 5


def run_selenium_init(url_to_scrape: str, headless: bool = False):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")  # Not used
    driver = webdriver.Chrome(options=options)

    driver.get(url_to_scrape)
    return driver


def run_selenium_login(driver, username: str, password: str):
    time.sleep(5)
    try:
        WebDriverWait(driver, max_wait_time_in_seconds).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "usercentrics-root")
            )
        )
        accept_button = driver.execute_script(
            """
            return document.querySelector('div#usercentrics-root')\
            .shadowRoot\
            .querySelector('button[data-testid="uc-accept-all-button"]')
            """
        )
        if accept_button:
            accept_button.click()
    except NoSuchElementException as exception:
        logging.warning(exception)

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-backdrop")
        )
    )

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, "//input[@type='email']")
        )
    )
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(username)
    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, "//input[@type='password']")
        )
    )
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    driver.find_element(
        By.XPATH, "//*[text()[contains(.,'Anmelden')]]/ancestor::button"
    ).submit()


def get_authorization_bearer(driver) -> str:
    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, "//*[text()[contains(.,'Nebenkosten')]]")
        )
    )
    driver.find_elements(By.XPATH, "//*[text()[contains(.,'Nebenkosten')]]")[0].click()

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//div[text()[contains(.,'Verbräuche')]]")
        )
    )
    driver.find_elements(By.XPATH, "//div[text()[contains(.,'Verbräuche')]]")[0].click()
    all_cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie["name"]] = cookie["value"]

    regex_for_bearer_token = r"Bearer\s+[A-Za-z0-9_]+"

    javascripts_to_check = set()

    for item in driver.find_elements(By.TAG_NAME, "link"):
        if item.get_attribute("as") == "script":
            javascripts_to_check.add(item.get_attribute("href"))

    for script in javascripts_to_check:
        response = None
        try:
            if script.startswith("https://kundenportal.vivawest.de"):
                response = requests.get(script, cookies=cookies_dict)
            else:
                response = requests.get(script)
        except requests.exceptions.RequestException as e:
            logging.warning(f"request failed for {script}; {e}")
            raise
        if response and "bearer" in response.text.lower():
            match = re.search(regex_for_bearer_token, response.text)
            if match:
                return match.group(0)
        time.sleep(3)

    logging.error(f"Unable to find the Bearer token:")
    return ""


def run_selenium_logout(driver):
    # WebDriverWait(driver, max_wait_time_in_seconds).until(
    #     expected_conditions.visibility_of_element_located((By.ID, "user-menu"))
    # )
    # driver.find_element(By.ID, "user-menu").click()
    #
    # WebDriverWait(driver, max_wait_time_in_seconds).until(
    #     expected_conditions.element_to_be_clickable(
    #         (
    #             By.XPATH,
    #             "//a[contains(@class, 'dropdown-item') and contains(@class, 'logout')]",
    #         )
    #     )
    # )
    # driver.find_element(
    #     By.XPATH,
    #     "//a[contains(@class, 'dropdown-item') and contains(@class, 'logout')]",
    # ).click()

    driver.close()
