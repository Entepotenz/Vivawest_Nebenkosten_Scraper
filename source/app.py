import os

from flask import Flask

import data_extraction
import scraping

URL = "https://kundenportal.vivawest.de/"

app = Flask(__name__)

# launch with this command inside the `source` folder
# poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app


@app.route("/")
def get_as_html():
    username = os.environ.get("USERNAME", None)
    password = os.environ.get("PASSWORD", None)
    result = scraping.scrape_site(URL, username, password)
    return result


@app.route("/json")
def get_as_json():
    username = os.environ.get("USERNAME", None)
    password = os.environ.get("PASSWORD", None)
    result = scraping.scrape_site(URL, username, password)
    result = data_extraction.scrape_site_json(result)

    return result


if __name__ == "__main__":
    app.run(debug=True)
