import datetime
import os

from flask import Flask

import scraping

URL = "https://kundenportal.vivawest.de/"

app = Flask(__name__)

# launch with this command inside the `source` folder
# poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app


@app.route("/")
def get_as_html():
    return get_as_json()


@app.route("/json")
def get_as_json():
    username = os.environ.get("USERNAME", None)
    password = os.environ.get("PASSWORD", None)

    result = scraping.scrape_site(URL, username, password)
    result["heizenergie"] = reformat_data_for_month(result["heizenergie"])
    result["kaltwasser"] = reformat_data_for_month(result["kaltwasser"])

    return result


def reformat_data_for_month(data: list) -> dict[str, dict]:
    result = {}

    for item in data:
        parsed_date = datetime.datetime(item["jahr"], item["monat"], 1)
        keyname = parsed_date.strftime('%Y-%m')
        if keyname in result:
            raise ValueError(
                f'keyname is NOT unique; keyname:={keyname}; result["{keyname}"]:={result[keyname]}; item:={item}'
            )
        else:
            result[keyname] = item

    return result


if __name__ == "__main__":
    app.run(debug=True)
