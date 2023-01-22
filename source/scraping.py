from bs4 import BeautifulSoup

import selenium_code


def scrape_site(url_to_scrape: str, username: str, password: str) -> str:
    driver = selenium_code.run_selenium_first_step(url_to_scrape, username, password)
    src = driver.page_source

    result_html = """\
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
