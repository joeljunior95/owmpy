from owmpy import OpenWeatherMap
from dotenv import load_dotenv
import os

load_dotenv(".env")

api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

if __name__ == "__main__":
    weather = OpenWeatherMap(api_key,
                            "Campinas,SP,BR")

    forecasts = weather.weather_info(None)

    exit()