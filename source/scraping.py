import json

from bs4 import BeautifulSoup

import selenium_code


def scrape_site(url_to_scrape: str, username: str, password: str) -> dict:
    result = {}

    driver = selenium_code.run_selenium_first_step(url_to_scrape, username, password)
    result["heizenergie"] = extract_data_from_html(driver.page_source)

    driver = selenium_code.run_selenium_second_step(driver)
    result["kaltwasser"] = extract_data_from_html(driver.page_source)

    return result


def extract_data_from_html(html_src: str) -> dict:
    parser = BeautifulSoup(html_src, "html.parser")
    result_str = parser.findAll("canvas")[0]["data-response"]
    return json.loads(result_str)
