import unittest
import weather_station


class TestWeatherStation(unittest.TestCase):

    def test_str_to_float(self):
        self.assertEqual(weather_station.str_to_float("1.0"), 1.0)
        self.assertEqual(weather_station.str_to_float("non-float"), -1.0)

    def test_str_to_int(self):
        self.assertEqual(weather_station.str_to_int("1"), 1)
        self.assertEqual(weather_station.str_to_float("non-integer"), -1)

    def test_from_json(self):
        station = weather_station.WeatherStation()
        json_data = {
            "23": [
                {"Timestamp": "Feb 2011", "Value": "159.6"},
                {"Timestamp": "Mar 2011", "Value": "78.6"},
            ]
        }
        self.assertTrue(station.from_json(json_data))

    def test_years(self):
        station = weather_station.WeatherStation()
        json_data = {
            "23": [
                {"Timestamp": "Feb 2011", "Value": "159.6"},
                {"Timestamp": "Mar 2011", "Value": "78.6"},
            ]
        }
        station.from_json(json_data)
        self.assertListEqual(station.years(), [2011])

    def test_maximum_per_year(self):
        station = weather_station.WeatherStation()
        json_data = {
            "23": [
                {"Timestamp": "Feb 2011", "Value": "159.6"},
                {"Timestamp": "Mar 2011", "Value": "78.6"},
            ]
        }
        station.from_json(json_data)
        expected_measurement = station.measurements[0]
        expected_dict = {2011: expected_measurement}
        self.assertDictEqual(station.maximum_per_year(), expected_dict)


if __name__ == "__main__":
    unittest.main()
