"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = ""
__email__ = ""


from weather_data import WeatherData, WeatherDataItem
from math import inf as INF

EASTERLIES = ('NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE')

class WeatherPrediction(object) :
    """Superclass for all of the different weather prediction models."""
    
    def __init__(self, weather_data) :
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def chance_of_rain(self) :
        """(int) Percentage indicating chance of rain occuring."""
        raise NotImplementedError

    def high_temperature(self) :
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self) :
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self) :
        """(int) Expected humidity."""
        raise NotImplementedError

    def wind_speed(self) :
        """(int) Expected average wind speed."""
        raise NotImplementedError

    def cloud_cover(self) :
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError



class YesterdaysWeather(WeatherPrediction) :
    """Simple prediciton model, based on yesterday's weather."""
    
    def __init__(self, weather_data) :
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def chance_of_rain(self) :
        """(int) Percentage indicating chance of rain occuring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1;  LITTLE_RAIN = 3;  SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0;  MILD = 40;  PROBABLE = 75;  LIKELY = 90
        
        if self._yesterdays_weather.get_rainfall() < NO_RAIN :
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN :
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN :
            chance_of_rain = PROBABLE
        else :
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self) :
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self) :
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self) :
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self) :
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self) :
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()


# Your implementations of the SimplePrediction and SophisticatedPrediction
# classes should go here.
class SimplePrediction(WeatherPrediction) :
    """Simple Prediction"""
    
    def __init__(self, weather_data, number_days) :
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._size = min(number_days, weather_data.get_size())
        self._data = weather_data.get_data(self._size)

    def chance_of_rain(self) :
        """(int) Percentage indicating chance of rain occuring."""
        total = 0
        for item in self._data:
            total += item.get_rainfall()
        factor = total / self._size * 9
        return min(100, factor)

    def high_temperature(self) :
        """(float) Expected high temperature."""
        highest = -INF
        for item in self._data:
            if item.get_high_temperature() > highest:
                highest = item.get_high_temperature()
        return highest

    def low_temperature(self) :
        """(float) Expected low temperature."""
        lowest = INF
        for item in self._data:
            if item.get_low_temperature() < lowest:
                lowest = item.get_low_temperature()
        return lowest

    def humidity(self) :
        """(int) Expected humidity."""
        total = 0
        for item in self._data:
            total += item.get_humidity()
        return total /  self._size

    def wind_speed(self) :
        """(int) Expected average wind speed."""
        total = 0
        for item in self._data:
            total += item.get_average_wind_speed()
        return total /  self._size

    def cloud_cover(self) :
        """(int) Expected amount of cloud cover."""
        total = 0
        for item in self._data:
            total += item.get_high_temperature()
        return total /  self._size

class SophisticatedPrediction(SimplePrediction) :
    """Sophisticated Prediction."""
    
    def __init__(self, weather_data, number_days) :
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data, number_days)
        self._average_air_pressure = self.average_air_pressure()
        self._yesterday_pressure = self._weather_data.get_data(1)[0].get_air_pressure()

    def average_air_pressure(self):
        total = 0
        for item in self._data:
            total += item.get_air_pressure()
        return total / self._size

    def chance_of_rain(self) :
        """(int) Percentage indicating chance of rain occuring."""
        total = 0
        for item in self._data:
            total += item.get_rainfall()
        average_rain = total / self._size

        if self._yesterday_pressure < self._average_air_pressure:
            average_rain *= 10
        else:
            average_rain *= 7

        if self._weather_data.get_data(1)[0].get_wind_direction() in EASTERLIES:
            average_rain *= 1.2

        return min(100, average_rain)

    def high_temperature(self) :
        """(float) Expected high temperature."""
        total = 0
        for item in self._data:
            total += item.get_high_temperature()
        average_high = total / self._size

        if self._yesterday_pressure > self._average_air_pressure:
            average_high += 2

        return average_high


    def low_temperature(self) :
        """(float) Expected low temperature."""
        total = 0
        for item in self._data:
            total += item.get_low_temperature()
        average_low = total / self._size

        if self._yesterday_pressure < self._average_air_pressure:
            average_low -= 2

        return average_low

    def humidity(self) :
        """(int) Expected humidity."""
        average_humidity = super().humidity()

        if self._yesterday_pressure < self._average_air_pressure:
            average_humidity += 15
        else:
            average_humidity -= 15

        return max(0, min(100, average_humidity))

    def wind_speed(self) :
        """(int) Expected average wind speed."""
        average_wind = super().wind_speed()

        if self._weather_data.get_data(1)[0].get_max_wind_speed() > 4 * average_wind:
            average_wind *= 1.2

        return average_wind

    def cloud_cover(self) :
        """(int) Expected amount of cloud cover."""
        average_cloud = super().cloud_cover()

        if self._yesterday_pressure < self._average_air_pressure:
            average_cloud += 2

        return min(9, average_cloud)

if __name__ == "__main__" :
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
