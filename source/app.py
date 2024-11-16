import os

import scraping

URL = "https://kundenportal.vivawest.de/"

# launch with this command inside the `source` folder
# poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app


def get_as_html():
    return get_as_json()


def get_as_json():
    username = os.environ.get("USERNAME", None)
    password = os.environ.get("PASSWORD", None)

    return scraping.scrape_site(URL, username, password)
