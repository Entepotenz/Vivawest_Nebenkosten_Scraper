from bs4 import BeautifulSoup


def extract_heizenergie(html_source: str) -> str:
    result_html = "<section>"
    result_html += "<h1>Heizenergie</h1>"

    parser = BeautifulSoup(html_source, "html.parser")
    tables = parser.findAll("table")

    for table in tables:
        if (
                table.findParent("table") is None
                and "table-striped" in table.attrs["class"]
        ):
            result_html += str(table)

    result_html += "</section>"

    return result_html


def extract_kaltwasser(html_source: str) -> str:
    result_html = "<section>"
    result_html += "<h1>Kaltwasser</h1>"

    parser = BeautifulSoup(html_source, "html.parser")
    tables = parser.findAll("table")

    for table in tables:
        if (
                table.findParent("table") is None
                and "table-striped" in table.attrs["class"]
        ):
            result_html += str(table)

    result_html += "</section>"

    return result_html
