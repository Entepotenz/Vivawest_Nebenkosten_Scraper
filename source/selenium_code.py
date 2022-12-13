import time
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def run_selenium_first_step(SAMPLE_URL: str, username: str, password: str):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")
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

    driver.get(SAMPLE_URL)
    time.sleep(5)  # TODO: remove this
    maxWaitTimeInSeconds = 5  # seconds
    try:
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.presence_of_element_located((By.ID, "usercentrics-root"))
        )
        driver.execute_script(
            """return document.querySelector('div#usercentrics-root').shadowRoot.querySelector('button[data-testid="uc-accept-all-button"]')"""
        ).click()
    except NoSuchElementException as e:
        logging.warning(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop"))
    )

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located((By.ID, "login-username"))
    )
    driver.find_element(By.ID, "login-username").send_keys(username)
    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located((By.ID, "login-password"))
    )
    driver.find_element(By.ID, "login-password").send_keys(password)
    driver.find_element(By.ID, "loginForm").submit()

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop"))
    )

    try:
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.element_to_be_clickable(
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
    except Exception as e:
        logging.exception(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop"))
    )

    try:
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[text()[contains(.,"Verbräuche")]]')
            )
        )
        driver.find_element(By.XPATH, '//*[text()[contains(.,"Verbräuche")]]').click()
    except Exception as e:
        logging.exception(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.element_to_be_clickable((By.ID, "logo"))
    )

    try:
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[text()[contains(.,"Zu den Details")]]')
            )
        )
        driver.find_element(
            By.XPATH, '//*[text()[contains(.,"Zu den Details")]]'
        ).click()
    except Exception as e:
        logging.exception(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.element_to_be_clickable((By.ID, "logo"))
    )

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-backdrop"))
    )

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[text()[contains(.,"Verbrauch der letzten")]]')
        )
    )

    return driver


def run_selenium_second_step(driver):
    maxWaitTimeInSeconds = 5  # seconds
    select = Select(
        driver.find_element(
            By.XPATH,
            '//*[text()[contains(.,"Verbrauchsart auswählen")]]/parent::div/child::select',
        )
    )
    select.select_by_visible_text("Kaltwasser")

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[text()[contains(.,"Verbrauch der letzten")]]')
        )
    )
    return driver


def run_selenium_logout(driver):
    maxWaitTimeInSeconds = 5  # seconds
    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located((By.ID, "user-menu"))
    )
    driver.find_element(By.ID, "user-menu").click()

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.element_to_be_clickable(
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
