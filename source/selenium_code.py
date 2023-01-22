import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def run_selenium_first_step(url_to_scrape: str, username: str, password: str):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1280,720")
    # options.add_argument("--window-size=800,600")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")  # Not used
    driver = webdriver.Chrome(options=options)

    # implicit wait tells WebDriver to poll the DOM for a certain amount of time
    # when trying to find any element (or elements) not immediately available.
    # The default setting is 0 (zero).
    # Once set, the implicit wait is set for the life of the WebDriver object.
    driver.implicitly_wait(10)

    driver.get(url_to_scrape)
    time.sleep(5)  # TODO: remove this
    max_wait_time_in_seconds = 5  # seconds
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

    try:
        WebDriverWait(driver, max_wait_time_in_seconds).until(
            expected_conditions.element_to_be_clickable(
                (
                    By.XPATH,
                    '//a[text()[contains(.,"Nebenkosten")]]',
                )
            )
        )
        driver.find_element(
            By.XPATH,
            '//a[text()[contains(.,"Nebenkosten")]]',
        ).click()
    except Exception as exception:
        logging.exception(exception)

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-backdrop")
        )
    )

    try:
        WebDriverWait(driver, max_wait_time_in_seconds).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//*[text()[contains(.,"Verbräuche")]]')
            )
        )
        driver.find_element(By.XPATH, '//*[text()[contains(.,"Verbräuche")]]').click()
    except Exception as exception:
        logging.exception(exception)

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, "logo"))
    )

    try:
        WebDriverWait(driver, max_wait_time_in_seconds).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//*[text()[contains(.,"Zu den Details")]]')
            )
        )
        driver.find_element(
            By.XPATH, '//*[text()[contains(.,"Zu den Details")]]'
        ).click()
    except Exception as exception:
        logging.exception(exception)

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, "logo"))
    )

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-backdrop")
        )
    )

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, '//*[text()[contains(.,"Verbrauch der letzten")]]')
        )
    )

    select = Select(
        driver.find_element(
            By.XPATH,
            '//*[text()[contains(.,"Vergleich Vorjahr")]]/parent::select',
        )
    )
    select.select_by_visible_text("Vergleich Liegenschaft")

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.element_to_be_clickable((By.ID, "logo"))
    )

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".modal-backdrop")
        )
    )

    return driver


def run_selenium_second_step(driver):
    max_wait_time_in_seconds = 5  # seconds
    select = Select(
        driver.find_element(
            By.XPATH,
            '//*[text()[contains(.,"Verbrauchsart auswählen")]]/parent::div/child::select',
        )
    )
    select.select_by_visible_text("Kaltwasser")

    select = Select(
        driver.find_element(
            By.XPATH,
            '//*[text()[contains(.,"Vergleich Vorjahr")]]/parent::select',
        )
    )
    select.select_by_visible_text("Vergleich Liegenschaft")

    WebDriverWait(driver, max_wait_time_in_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.XPATH, '//*[text()[contains(.,"Verbrauch der letzten")]]')
        )
    )
    return driver


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
