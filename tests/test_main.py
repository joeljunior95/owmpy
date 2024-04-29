from dotenv import load_dotenv
import os
import pytest

from owmpy import OpenWeatherMap
from owmpy.errors import OWMException

load_dotenv(".env")

api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

def test_forecast():
    weather = OpenWeatherMap(api_key,"Campinas,SP,BR")

    forecasts = weather.weather_info(None)

    assert len(forecasts) > 0
    assert len(forecasts) == 6

def test_invalid_locaton():
    with pytest.raises(OWMException):
        weather = OpenWeatherMap(api_key,"inv,al,id")

        forecasts = weather.weather_info(None)