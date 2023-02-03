import json
from datetime import datetime

from bs4 import BeautifulSoup


def extract_heizenergie(html_source: str) -> str:
    return extract_data_from_table_generic(html_source, "Heizenergie")


def extract_data_from_table_generic(html_source: str, header_name: str) -> str:
    result_html = "<section>"
    result_html += f"<h1>{header_name}</h1>"

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


def extract_heizenergie_generic(data: dict, tag: str, section_header_name: str) -> str:
    extracted_data_filtered = filter(lambda x: (tag in x), data)
    extracted_data_mapped = map(
        lambda x: {
            "monat": x.get("monat"),
            "jahr": x.get("jahr"),
            "table_header": datetime.strptime(
                f"{x.get('monat')} {x.get('jahr')}", "%m %Y"
            ).strftime("%b %y"),
            "table_value": x.get(tag),
        },
        extracted_data_filtered,
    )
    extracted_data = list(extracted_data_mapped)

    result_html = "<section>"
    result_html += f"<h1>{section_header_name}</h1>"

    result_html += '<table class="table table-striped">'

    result_html += "<thead>"
    result_html += "<tr>"
    for item in extracted_data:
        result_html += f"<th>{item.get('table_header')}</th>"
    result_html += "<tr>"
    result_html += "</thead>"

    result_html += "<tbody>"
    result_html += "<tr>"
    for item in extracted_data:
        result_html += f"<td>{item.get('table_value')}</td>"
    result_html += "</tbody>"

    result_html += "</table>"

    result_html += "</section>"

    return result_html


def extract_heizenergie_liegenschaft_kwh(html_source: str) -> str:
    data = extract_json_from_canvas(html_source)

    result_html = extract_heizenergie_generic(
        data, "verbrauchswert_liegenschaft_qm_kwh", "verbrauchswert_liegenschaft_qm_kwh"
    )
    result_html += extract_heizenergie_generic(
        data,
        "verbrauchswert_liegenschaft_geraete_kwh",
        "verbrauchswert_liegenschaft_geraete_kwh",
    )

    return result_html


def extract_kaltwasser(html_source: str) -> str:
    return extract_data_from_table_generic(html_source, "Kaltwasser")


def extract_kaltwasser_liegenschaft_m3(html_source: str) -> str:
    data = extract_json_from_canvas(html_source)

    result_html = extract_heizenergie_generic(
        data,"verbrauchswert_liegenschaft_geraete",
        "verbrauchswert_liegenschaft_geraete_wasser",
    )
    result_html += extract_heizenergie_generic(
        data, "verbrauchswert_liegenschaft_qm", "verbrauchswert_liegenschaft_qm_wasser"
    )

    return result_html


def extract_json_from_canvas(html_source: str) -> dict:
    parser = BeautifulSoup(html_source,      "html.parser")
    canvas = parser.find("canvas", {"id": "bar-chart"})
    return json.loads(canvas.attrs.get(   "data-response"  ))
