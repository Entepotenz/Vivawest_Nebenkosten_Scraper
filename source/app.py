import logging
import os

from flask import Flask
import scraping

URL = 'https://kundenportal.vivawest.de/'

app = Flask(__name__)

# launch with this command inside the `source` folder
# poetry run gunicorn --bind 0.0.0.0:8080 --timeout 90 --reload app:app


@app.route('/')
def home():
    username = os.environ.get('USERNAME', None)
    password = os.environ.get('PASSWORD', None)
    result = scraping.scrape_site(URL, username, password)
    return result


@app.route('/json')
def getAsJson():
    username = os.environ.get('USERNAME', None)
    password = os.environ.get('PASSWORD', None)
    result = scraping.scrape_site_json(URL, username, password)

    return result


if __name__ == '__main__':
    app.run(debug=True)
