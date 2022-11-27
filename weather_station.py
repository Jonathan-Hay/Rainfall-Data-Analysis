import json


def str_to_int(input_string):
    """
    A function that takes a string as input and returns an integer.
    If a non-integer value is entered as a string, the function returns -1.
    """

    try:
        return int(input_string)
    except ValueError:
        return -1


def str_to_float(input_string):
    """
    A function that takes a string as input and returns a float.
    If a non-float value is entered as a string, the function returns -1.0.
    """

    try:
        return float(input_string)
    except ValueError:
        return -1.0


def month_to_int(input_month):
    """
    A function that takes a given month prefix and returns
    the corresponding integer value. If an invalid prefix
    is entered, -1 is returned.
    """

    months_and_integer = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    return months_and_integer.get(input_month, -1)


class Measurement:
    """
    A class to represent a measurement of rainfall for a given month and year.
    """

    def __init__(self):
        self.year = 0
        self.month = 0
        self.value = 0.0

    def __repr__(self):
        s = "{"
        s += f"year:{self.year},"
        s += f"month:{self.month},"
        s += f"value:{self.value}"
        s += "}"
        return s

    def from_strings(self, year_str, month_str, value_str):
        """
        A function to convert input strings to integers for the month and year,
        and a float for the associated value. True or false is returned
        depending on the success of the conversion.
        """

        self.year = str_to_int(year_str)
        self.month = month_to_int(month_str)
        self.value = str_to_float(value_str)

        if self.year == -1 or self.month == -1 or self.value == -1.0:
            return False
        else:
            return True


class WeatherStation:
    """
    A class to represent a weather station and its associated measurements.
    """

    def __init__(self):
        self.id = 0
        self.measurements = []

    def __repr__(self):

        s = f"staion id:{self.id},"
        s += f"measurements:{self.measurements}"
        return s

    def from_json(self, data):
        """
        A function to fill the classes data members from input JSON.
        The function returns true or false depending on if the data
        was successfully read or not.
        """

        if len(data) != 1:
            return False

        for key in data:
            self.id = str_to_int(key)
            if self.id == -1:
                return False

            for measurement in data[key]:
                month_and_year = measurement["Timestamp"].split(" ")
                month = month_and_year[0]
                year = month_and_year[1]
                value = measurement["Value"]
                measurement_object = Measurement()

                if not measurement_object.from_strings(year, month, value):
                    return False
                self.measurements.append(measurement_object)

        return True

    def years(self):
        """
        A function that returns a list of each of the years
        in which rainfall data was collected.
        """

        unique_years = []

        for measurement_object in self.measurements:
            if measurement_object.year not in unique_years:
                unique_years.append(measurement_object.year)
        return unique_years

    def maximum_per_year(self):
        """
        Returns a dictionary of years and their corresponding
        measurement object representing the highest rainfall for that year.
        """

        years_and_max_value = {}

        for measurement_object in self.measurements:
            value_to_check = years_and_max_value.get(measurement_object.year)
            if (value_to_check is None or
                    value_to_check.value < measurement_object.value):
                years_and_max_value[measurement_object.year] =\
                    measurement_object
        return years_and_max_value


"""
A program to load the JSON file and find, for the given weather station,
the years in which measurements were taken and greatest measurement
for each year.
"""
if __name__ == "__main__":
    with open("rainfall.json") as file:
        data = json.load(file)
    station = WeatherStation()
    station.from_json(data)
    print(station.years())
    print(station.maximum_per_year())
