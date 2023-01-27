import locale
import re
from pathlib import Path

import dateutil.parser
from bs4 import BeautifulSoup


def scrape_site_json(html_table: str) -> dict:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    result_dict = {}

    parser = BeautifulSoup(html_table, "html.parser")

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
                    value = convert_to_float(value)
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
        ("Sep", "September", "Sept"),
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
        # locale.atof is not working correctly on alpine "," "." conversion -> if detected fix it manually
        if is_running_on_alpine() and re.search(r"^\d+,\d+$", input):
            input = input.replace(",", ".")
        _ = locale.atof(input)
    except (TypeError, ValueError):
        return False
    else:
        return True


def convert_to_float(input: str) -> float:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    if is_running_on_alpine() and re.search(r"^\d+,\d+$", input):
        input = input.replace(",", ".")
    return locale.atof(input)


def is_int(input: str) -> bool:
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    try:
        a = locale.atof(input)
        b = int(input)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


def is_running_on_alpine() -> bool:
    alpine_release_file = Path("/etc/alpine-release")
    if alpine_release_file.exists():
        if alpine_release_file.stat().st_size != 0:
            return True

    return False