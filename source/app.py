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
    headless_env = os.getenv("SELENIUM_HEADLESS", "true")
    headless = str(headless_env).lower() in ("1", "true", "yes", "y")

    return scraping.scrape_site(URL, username, password, headless)
