"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = ""
__email__ = ""


from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, \
    SophisticatedPrediction
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


class Event(object):
    """Represents details about an event that may be influenced by weather."""

    def __init__(self, time, outdoors, cover_available, name):
        """
        Parameters:
            time (int): Closest hour of starting time, in 24 hour format.
            outdoors (bool): Is the event being held outdoors.
            cover_available (bool): Is there covered shelter for participants.
            name (str): Descriptive name of the event.

        Pre-condition:
            0 <= time < 24
        """
        self._time = time
        self._outdoors = outdoors
        self._cover_available = cover_available
        self._name = name

    def get_time(self):
        """(int) Return the hour closest to the starting time of the event."""
        return self._time

    def get_outdoors(self):
        """(bool) Return if the event is being held outdoors."""
        return self._outdoors

    def get_cover_available(self):
        """(bool) Return if there is covered shelter for participants."""
        return self._cover_available

    def get_name(self):
        """(str) Return the name describing this event."""
        return self._name

    def __str__(self):
        return f'Event({self._name} @ {self._time}, {self._outdoors}, {self._cover_available})'


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           A subclass of WeatherPrediction used to predict
                           the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (int) Temperature Factor
        """
        humidity_factor = 0
        if self._prediction_model.humidity() > 70:
            humidity_factor = self._prediction_model / 20

        high = self._prediction_model.high_temperature()
        low = self._prediction_model.low_temperature()
        time = self._event.get_time()

        if high >= 0:
            high += humidity_factor
        else:
            high -= humidity_factor

        if low >= 0:
            low += humidity_factor
        else:
            low -= humidity_factor

        temp_factor = 0
        if high > 45 or (high > 30 and 6 <= time <= 19):
            temp_factor = high / -5 + 6
        if (0 <= time <= 5 or 20 <= time <= 23) and low < 5:
            temp_factor = low / 5 - 1.1
        if low > 15 and high < 30:
            temp_factor = (high - low) / 5

        if temp_factor < 0:
            if self._event.get_cover_available():
                temp_factor += 1
            if 3 < self._prediction_model.wind_speed() < 10:
                temp_factor += 1
            if self._prediction_model.cloud_cover() > 4:
                temp_factor += 1
        
        return temp_factor

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (int) Rain Factor
        """
        rain_chance = self._prediction_model.get_rain_chance()

        rain_factor = 0
        if rain_chance < 20:
            rain_factor = rain_chance / -5 + 4
        if rain_chance > 50:
            rain_factor = rain_chance / -20 + 1

        if self._event.get_outdoors() and self._event.get_cover_available() and \
            self._prediction_model().get_wind_speed() < 5:
            rain_factor += 1
        if rain_factor < 2 and self._prediction_model.get_wind_speed() > 15:
            rain_factor += self._prediction_model.get_wind_speed() / 15

        return max(rain_factor, -9)

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (int) Value in range of -5 to +5,
                  -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        advisability = min(max(self._rain_factor() + self._temperature_factor(), -5), 5)
        return advisability


class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """
        """
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        time = int(input('What time is the event? '))
        outdoors = bool(input('Is the event outdoors? '))
        cover_available = bool(input('Is there covered shelter? '))
        name = input('What is the name of the event? ')
        return Event(time, outdoors, cover_available, name)

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        models = {"1": YesterdaysWeather(weather_data),
                  "2": SimplePrediction(weather_data, 3),
                  "3": SimplePrediction(weather_data, 5),
                  "4": SophisticatedPrediction(weather_data, 5)
                  }

        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.")
        print("  2) Simple prediction based on past 3 days")
        print("  2) Simple prediction based on past 5 days")
        print("  2) Sophisticated prediction based on past 5 days")
        # Add in choices for other prediction models when they're implemented.
        model_choice = input(">")
        # Error handling can be added to this method.
        self._prediction_model = models[model_choice]
        return models[model_choice]

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (int): Impact of the weather on the event.
                          -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        decider = EventDecision(self._event, self._prediction_model)
        model_name = type(self._prediction_model).__name__
        print(f'Based on the {model_name} model, the advisability is {decider.advisability()}')

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediciton model.
        """
        return bool(input('Would you like to check again?'))


def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
