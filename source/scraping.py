import locale

import dateutil.parser
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


def scrape_site_json(url_to_scrape: str, username: str, password: str) -> dict:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    result = scrape_site(
        url_to_scrape=url_to_scrape, username=username, password=password
    )
    result_dict = {}

    parser = BeautifulSoup(result, "html.parser")

    sections = parser.find_all("section")

    for section in sections:
        data = {}

        title = section.find("h1")
        title = title.string.strip()

        table = section.find("table")
        headings = []
        for th in table.find("thead").find_all("th"):
            value = th.string.strip()
            if is_date(value):
                # fix year
                value = value.replace(" 21", "2021")
                value = value.replace(" 22", "2022")
                value = value.replace(" 23", "2023")
                value = value.replace(" 24", "2024")
                value = value.replace(" 25", "2025")
                value = value.replace(" 26", "2026")
                value = dateutil.parser.parse(
                    value, fuzzy=True, parserinfo=GermanLocaleParserInfo()
                )
                value = value.replace(day=1)  # we do not have day information
                value = value.isoformat()

            headings.append(value)

        for i in range(len(headings)):
            value = table.find("tbody").find("tr").find_all(["th", "td"])[i]
            if value.find("span", class_="cursor-help") is None:
                data[headings[i]] = value.string.strip()

        data["datapoints"] = {}
        for key in list(data.keys()):
            value = data.pop(key)
            if is_date(key):
                if is_float(value):
                    value = locale.atof(value)
                elif is_int(value):
                    value = int(value)

                data["datapoints"][key] = value
            else:
                data[key] = value

        result_dict[title] = data

    return result_dict


class GermanLocaleParserInfo(dateutil.parser.parserinfo):
    MONTHS = [
        ("Jan", "Januar", "January", "Jänner"),
        ("Feb", "Februar", "February"),
        ("Mrz", "März", "March", "Mar", "Mär"),
        ("Apr", "April"),
        ("Mai", "May"),
        ("Jun", "Juni", "June"),
        ("Jul", "Juli", "July"),
        ("Aug", "August"),
        ("Sep", "September"),
        ("Okt", "Oktober", "October", "Oct"),
        ("Nov", "November"),
        ("Dez", "Dezember", "Dec", "December"),
    ]


def is_date(input: str) -> bool:
    try:
        dateutil.parser.parse(input, fuzzy=True)
        return True
    except dateutil.parser.ParserError:
        return False


def is_float(input: str) -> bool:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    try:
        _ = locale.atof(input)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_int(input: str) -> bool:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    try:
        a = locale.atof(input)
        b = int(input)
    except (TypeError, ValueError):
        return False
    else:
        return a == b
