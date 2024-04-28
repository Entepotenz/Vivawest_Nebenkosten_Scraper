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

    return scraping.scrape_site(URL, username, password)


if __name__ == "__main__":
    app.run(debug=True)
