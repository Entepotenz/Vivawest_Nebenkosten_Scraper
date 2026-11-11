import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

max_wait_time_in_seconds = 5


def run_selenium_init(url_to_scrape: str, headless: bool = True):
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
        reject_button = driver.execute_script("""
            return document.querySelector('div#usercentrics-root')\
            .shadowRoot\
            .querySelector('button[data-testid="uc-deny-all-button"]')
            """)
        if reject_button:
            reject_button.click()
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

    WebDriverWait(driver, 30).until(
        lambda browser: browser.execute_script(
            "return JSON.parse(window.localStorage.getItem('user') || '{}').sessionId;"
        ),
        message="Login did not provide a sessionId in localStorage within 30 seconds",
    )


def get_cookies(driver) -> dict:
    all_cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie["name"]] = cookie["value"]
    return cookies_dict


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
