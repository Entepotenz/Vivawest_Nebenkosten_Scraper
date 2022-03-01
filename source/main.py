import logging
import os

import scraping

URL = 'https://kundenportal.vivawest.de/'

# launch with this command inside the `source` folder
# poetry run python main.py


def main() -> int:
    username = os.environ.get('USERNAME', None)
    password = os.environ.get('PASSWORD', None)

    result = scraping.scrape_site(URL, username, password)
    print(result)
    return 0


if __name__ == '__main__':
    main()
