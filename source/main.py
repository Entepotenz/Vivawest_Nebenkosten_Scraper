import logging
import os
import json
import sys

import scraping

URL = "https://kundenportal.vivawest.de/"

# launch with this command inside the `source` folder
# poetry run python main.py


def main(argv) -> int:
    username = os.environ.get("USERNAME", None)
    password = os.environ.get("PASSWORD", None)

    if len(argv) > 0 and argv[0] == "json":
        result = scraping.scrape_site_json(URL, username, password)
        result = json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False)
    else:
        result = scraping.scrape_site(URL, username, password)

    print(result)
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
