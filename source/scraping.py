import os
from pathlib import Path

from bs4 import BeautifulSoup

import selenium_code


def scrape_site(url_to_scrape: str, username: str, password: str) -> str:
    driver = selenium_code.run_selenium_first_step(url_to_scrape, username, password)
    src = driver.page_source

    filepath_of_test_input = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "resources", "html_head_style.html"
    )
    html_head_style = Path(filepath_of_test_input).read_text()

    result_html = f"""\
        <!DOCTYPE html>
        <html>
            {html_head_style}
        <body>
        """
    result_html += "<section>"
    result_html += "<h1>Heizenergie</h1>"
    parser = BeautifulSoup(src, "html.parser")
    tables = parser.findAll("table")
    for table in tables:
        if (
            table.findParent("table") is None
            and "table-striped" in table.attrs["class"]
        ):
            result_html += str(table)

    driver = selenium_code.run_selenium_second_step(driver)
    src = driver.page_source

    result_html += "</section>"
    result_html += "<section>"
    result_html += "<h1>Kaltwasser</h1>"

    parser = BeautifulSoup(src, "html.parser")
    tables = parser.findAll("table")
    for table in tables:
        if (
            table.findParent("table") is None
            and "table-striped" in table.attrs["class"]
        ):
            result_html += str(table)

    result_html += "</section>"
    result_html += "</body>"
    result_html += "</html>"

    selenium_code.run_selenium_logout(driver)

    # prettify html output
    parser = BeautifulSoup(result_html, "html.parser")
    result_html = parser.prettify()
    return result_html
