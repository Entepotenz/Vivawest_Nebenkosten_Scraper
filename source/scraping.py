import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def scrape_site(SAMPLE_URL: str, username: str, password: str):
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")
    # options.add_argument("--window-size=800,600")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')  # Not used
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
            EC.presence_of_element_located(
                (By.ID, 'cookie-consent-accept-selected')))
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.element_to_be_clickable(
                (By.ID, 'cookie-consent-accept-selected')))
        driver.find_element_by_id('cookie-consent-accept-selected').click()
        # wait until we do not see the cookie banner anymore
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.invisibility_of_element_located(
                (By.ID, 'cookie-consent-accept-selected')))
    except NoSuchElementException as e:
        logging.warning(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '.modal-backdrop')))

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located((By.ID, "login-username")))
    driver.find_element_by_id('login-username').send_keys(username)
    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located((By.ID, "login-password")))
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_id('loginForm').submit()

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '.modal-backdrop')))

    try:
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//a[text()="\n\t\t\t\t\t\t\t\t\t\tNebenkosten\n\t\t\t\t\t\t\t\t\t"]'
            )))
        driver.find_element(
            By.XPATH,
            '//a[text()="\n\t\t\t\t\t\t\t\t\t\tNebenkosten\n\t\t\t\t\t\t\t\t\t"]'
        ).click()
    except Exception as e:
        logging.exception(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '.modal-backdrop')))

    try:
        WebDriverWait(driver, maxWaitTimeInSeconds).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '/html/body/div[1]/div/div/div/div/div[2]/div/ul/li[2]/a')))
        driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div/div/div[2]/div/ul/li[2]/a').click()
    except Exception as e:
        logging.exception(e)

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.element_to_be_clickable((By.ID, "logo")))

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '.modal-backdrop')))

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "/html/body/div[1]/div/div/div/div/form/div[4]/div/div/div")))

    src = driver.page_source

    result = '''\
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <style type="text/css">
                    body{
                        margin:40px
                        auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px
                    }
                    h1,h2,h3{
                        line-height:1.2
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }

                    td, th {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }

                    tr:nth-child(even) {
                        background-color: #dddddd;
                    }
                </style>
            </head>
        <body>
        '''
    result += "<h1>Heizenergie</h1>"
    parser = BeautifulSoup(src, "html.parser")
    tables = parser.findAll("table")
    for table in tables:
        if table.findParent(
                "table") is None and 'table-striped' in table.attrs['class']:
            result += str(table)

    select = Select(driver.find_element_by_id('uvi-type'))
    select.select_by_visible_text('Kaltwasser')

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located(
            (By.XPATH,
             "/html/body/div[1]/div/div/div/div/form/div[4]/div/div/div")))

    result += "<h1>Kaltwasser</h1>"

    src = driver.page_source
    parser = BeautifulSoup(src, "html.parser")
    tables = parser.findAll("table")
    for table in tables:
        if table.findParent(
                "table") is None and 'table-striped' in table.attrs['class']:
            result += str(table)

    result += "</body>"
    result += "</html>"

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.visibility_of_element_located((By.ID, "user-menu")))
    driver.find_element_by_id('user-menu').click()

    WebDriverWait(driver, maxWaitTimeInSeconds).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class, 'dropdown-item') and contains(@class, 'logout')]"
        )))
    driver.find_element(
        By.XPATH,
        "//a[contains(@class, 'dropdown-item') and contains(@class, 'logout')]"
    ).click()

    driver.close()

    # prettify html output
    parser = BeautifulSoup(result, "html.parser")
    result = parser.prettify()
    return result
