from typing import List, Union
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests import request

from .errors import GernericOWMException, InvalidAPIKeyException, OWMException, OWMServerException, RequestLimitException, SearchParamsException
from .models import Geolocation, DaySummary

class OpenWeatherMap:
    def __init__(self, 
                 api_key: str, 
                 location: str,
                 units: str = "metric",
                 lang: str = "pt_br"):
            
        self.api_key = api_key
        self.city = ""
        self.state = ""
        self.country = ""
        self.api_host = "api.openweathermap.org"
        self.location = location
        self._daySummary = None
        self._geolocation = None
        self.units = units
        self.lang = lang

    @property
    def location(self) -> str:
        loc = ""

        if self.city != "":
            loc += self.city

        if self.state != "":
            if loc != "":
                loc += ","
            loc += self.state

        if self.country != "":
            if loc != "" and loc[-1] != ",":
                loc += ","
            loc += self.country

        return loc

    @location.setter
    def location(self, q: str):
        locs = q.split(",")
        while len(locs) < 3:
            locs.append("")

        self.city = locs[0].strip()
        self.state = locs[1].strip()
        self.country = locs[2].strip()

    @property
    def geolocation(self) -> Geolocation:
        if isinstance(self._geolocation, Geolocation):
            return self._geolocation
        
        data = None
        url = f"https://{self.api_host}/geo/1.0/direct"
        params = {
            "q": self.location,
            "appid": self.api_key,
            "limit": 1
        }
        response = request("get", url, params=params)
        if response.status_code == 200:
            jsonData = response.json()
            if len(jsonData) > 0:
                data = jsonData[0]
        
        self._geolocation = Geolocation(**data)
        return self._geolocation

    @property
    def daySummary(self) -> DaySummary:
        if isinstance(self._daySummary, DaySummary) and self._daySummary.date == self._date:
            return self._daySummary
        
        data = None
        dt = self._date.strftime("%Y-%m-%d")
        url = f"https://{self.api_host}/data/3.0/onecall/day_summary"
        params = {
            "lat": self.geolocation.lat,
            "lon": self.geolocation.lon,
            "appid": self.api_key,
            "units": self.units,
            "lang": self.lang,
            "date": dt
        }
        response = request("get", url, params=params)
        status_code = response.status_code
        match status_code:
            case 200:
                data = response.json()
            case 401:
                raise InvalidAPIKeyException(
                    f"The API Key informed is not valid or is not activated yet. {response.status_code} {response.reason} {response.content}"
                )
            case 404:
                raise SearchParamsException(
                    f"The params informed incorrect. {response.status_code} {response.reason} {response.content}"
                )
            case 429:
                raise RequestLimitException(
                    f"You have exceeded the api calls limit of your plan. {response.status_code} {response.reason} {response.content}"
                )
            case 500 | 502 | 503 | 504:
                raise OWMServerException(
                    f"There's a problem with the OpenWeatherMap server. Please, contact them for more information. {response.status_code} {response.reason} {response.content}"
                )
            case _:
                raise GernericOWMException(
                    f"{response.status_code} {response.reason} {response.content}"
                )
        
        self._daySummary = DaySummary(**data)
        return self._daySummary
    
    def weather_info(self, 
                     date: Union[str | datetime | None], 
                     days_forward: int = 5) -> List[DaySummary]:
        daySummaryList: List[DaySummary] = []

        if date is None:
            self._date = datetime.now()
        elif isinstance(date,str):
            self._date = datetime.strptime(date,"%Y-%m-%d")
        else:
            self._date = date

        day_loop = 0
        while day_loop <= days_forward:
            daySummaryList.append(self.daySummary)

            self._date += relativedelta(days=1)
            day_loop += 1


        return daySummaryList
    

    