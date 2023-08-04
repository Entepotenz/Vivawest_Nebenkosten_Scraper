import json
import sys

import app

# launch with this command inside the `source` folder
# poetry run python main.py


def main(argv) -> int:
    result = app.get_as_json()

    print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
