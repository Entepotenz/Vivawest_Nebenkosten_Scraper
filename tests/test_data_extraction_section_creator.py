import os
import unittest
from pathlib import Path

from source.data_extraction import scrape_site_json
from source.data_extraction_section_creator import (
    extract_heizenergie,
    extract_heizenergie_liegenschaft_kwh,
    extract_kaltwasser,
    extract_kaltwasser_liegenschaft_m3,
)


class MyTestCase(unittest.TestCase):
    _filepath_of_test_input_heizenergie = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "selenium_code_first_step_result.html",
    )
    _filepath_of_test_input_kaltwasser = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "selenium_code_second_step_result.html",
    )

    def test_extract_heizenergie_liegenschaft(self):
        input = Path(self._filepath_of_test_input_heizenergie).read_text()
        result = extract_heizenergie_liegenschaft_kwh(input)
        result = scrape_site_json(result)

        expected = {
            "verbrauchswert_liegenschaft_qm_kwh": {
                "datapoints": {
                    "2022-09-01T00:00:00": 117.75999999999999,
                    "2022-08-01T00:00:00": 90.52799999999999,
                    "2022-07-01T00:00:00": 94.208,
                    "2022-06-01T00:00:00": 91.264,
                    "2022-05-01T00:00:00": 119.96799999999999,
                    "2022-04-01T00:00:00": 253.18399999999997,
                    "2022-03-01T00:00:00": 335.61599999999993,
                    "2022-02-01T00:00:00": 401.856,
                    "2022-01-01T00:00:00": 535.0719999999999,
                }
            },
            "verbrauchswert_liegenschaft_geraete_kwh": {
                "datapoints": {
                    "2022-09-01T00:00:00": 1.6,
                    "2022-08-01T00:00:00": 1.23,
                    "2022-07-01T00:00:00": 1.28,
                    "2022-06-01T00:00:00": 1.24,
                    "2022-05-01T00:00:00": 1.63,
                    "2022-04-01T00:00:00": 3.44,
                    "2022-03-01T00:00:00": 4.56,
                    "2022-02-01T00:00:00": 5.46,
                    "2022-01-01T00:00:00": 7.27,
                }
            },
        }

        self.assertDictEqual(result, expected)

    def test_extract_heizenergie_eigen(self):
        input = Path(self._filepath_of_test_input_heizenergie).read_text()
        result = extract_heizenergie(input)
        result = scrape_site_json(result)

        expected = {
            "Heizenergie": {
                "Raum / Zähler-Nr.": "Abstellkammer (2054578)",
                "datapoints": {
                    "2022-01-01T00:00:00": 678.0,
                    "2022-02-01T00:00:00": 574.0,
                    "2022-03-01T00:00:00": 546.0,
                    "2022-04-01T00:00:00": 389.0,
                    "2022-05-01T00:00:00": 228.0,
                    "2022-06-01T00:00:00": 210.0,
                    "2022-07-01T00:00:00": 169.0,
                    "2022-08-01T00:00:00": 195.0,
                    "2022-09-01T00:00:00": 186.0,
                    "2022-12-01T00:00:00": 403.0,
                },
            }
        }

        self.assertDictEqual(result, expected)

    def test_extract_kaltwasser_liegenschaft(self):
        input = Path(self._filepath_of_test_input_kaltwasser).read_text()
        result = extract_kaltwasser_liegenschaft_m3(input)
        result = scrape_site_json(result)

        expected = {
            "verbrauchswert_liegenschaft_geraete_wasser": {
                "datapoints": {
                    "2022-09-01T00:00:00": 0.08,
                    "2022-08-01T00:00:00": 0.08,
                    "2022-07-01T00:00:00": 0.08,
                    "2022-06-01T00:00:00": 0.07,
                    "2022-05-01T00:00:00": 0.07,
                    "2022-04-01T00:00:00": 0.08,
                    "2022-03-01T00:00:00": 0.08,
                    "2022-02-01T00:00:00": 0.07,
                    "2022-01-01T00:00:00": 0.09,
                }
            },
            "verbrauchswert_liegenschaft_qm_wasser": {
                "datapoints": {
                    "2022-09-01T00:00:00": 5.888,
                    "2022-08-01T00:00:00": 5.888,
                    "2022-07-01T00:00:00": 5.888,
                    "2022-06-01T00:00:00": 5.152,
                    "2022-05-01T00:00:00": 5.152,
                    "2022-04-01T00:00:00": 5.888,
                    "2022-03-01T00:00:00": 5.888,
                    "2022-02-01T00:00:00": 5.152,
                    "2022-01-01T00:00:00": 6.624,
                }
            },
        }

        self.assertDictEqual(result, expected)

    def test_extract_kaltwasser_eigen(self):
        input = Path(self._filepath_of_test_input_kaltwasser).read_text()
        result = extract_kaltwasser(input)
        result = scrape_site_json(result)

        expected = {
            "Kaltwasser": {
                "Raum / Zähler-Nr.": "Abstellkammer (2067626)",
                "datapoints": {
                    "2022-01-01T00:00:00": 7.04,
                    "2022-02-01T00:00:00": 6.77,
                    "2022-03-01T00:00:00": 5.8,
                    "2022-04-01T00:00:00": 6.45,
                    "2022-05-01T00:00:00": 6.61,
                    "2022-06-01T00:00:00": 5.91,
                    "2022-07-01T00:00:00": 3.11,
                    "2022-08-01T00:00:00": 6.31,
                    "2022-09-01T00:00:00": 6.14,
                    "2022-12-01T00:00:00": 5.16,
                },
            }
        }

        self.assertDictEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
