import json
import logging
from http import HTTPStatus

import requests
import selenium_code


def scrape_site(
    url_to_scrape: str, username: str, password: str, headless: bool
) -> dict:
    result = {}

    driver = selenium_code.run_selenium_init(url_to_scrape, headless=headless)
    selenium_code.run_selenium_login(driver, username, password)
    bearer_token = selenium_code.get_authorization_bearer(driver)
    result["heizenergie"] = get_heizenergie(driver, bearer_token)
    result["kaltwasser"] = get_kaltwasser(driver, bearer_token)
    selenium_code.run_selenium_logout(driver)

    return result


def get_heizenergie(driver, bearer_token: str) -> dict:
    data = get_data_from_api(
        driver,
        "https://kundenportal.vivawest.de/api/uvi/current/heizenergie",
        bearer_token,
    )

    return transform_data(data)


def get_kaltwasser(driver, bearer_token: str) -> dict:
    data = get_data_from_api(
        driver,
        "https://kundenportal.vivawest.de/api/uvi/current/kaltwasser",
        bearer_token,
    )

    return transform_data(data)


def transform_data(data) -> dict:
    transformed_data = {}
    for messwert in data.get("messwerte"):
        month_as_string = str(messwert.get("monat"))
        if int(messwert.get("monat")) < 10:
            month_as_string = f'0{messwert.get("monat")}'

        transformed_data[f'{messwert.get("jahr")}-{month_as_string}'] = messwert

    return transformed_data


def get_data_from_api(driver, url: str, bearer_token: str) -> dict:
    session = create_requests_instance_from_selenium_driver(driver, bearer_token)
    response = session.get(url)

    if response.status_code == HTTPStatus.OK:
        return json.loads(response.content)
    else:
        logging.error(f"bad response: {response.status_code}")
        return {}


def create_requests_instance_from_selenium_driver(
    driver, bearer_token: str
) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Authorization": bearer_token})
    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])

    # Try to copy the 'user' key from localStorage into a cookie named 'fe_typo_user'
    try:
        local_user = driver.execute_script(
            "return window.localStorage.getItem('user');"
        )
        if local_user:
            sessionToken = json.loads(local_user).get("sessionToken", None)
            if sessionToken:
                session.cookies.set("fe_typo_user", sessionToken)
            else:
                logging.debug("no 'sessionToken' found in localStorage 'user' value")
        else:
            logging.debug("no localStorage 'user' value found")
    except Exception:
        logging.debug("could not read localStorage 'user' value", exc_info=True)

    return session
