from typing import List, Union
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests import request

from owmpy.errors import InvalidAPIKeyException
from owmpy.models import Geolocation, DaySummary

class OpenWeatherMap:
    def __init__(self, 
                 api_key: str, 
                 location: str,
                 units: str = "metric",
                 lang: str = "pt_br"):
        if api_key == "":
            raise InvalidAPIKeyException(f"API Key informed is not valid:{api_key}")
        else:
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
        if response.status_code == 200:
            data = response.json()
        
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

        day_loop = 1
        while day_loop <= days_forward:
            daySummaryList.append(self.daySummary)

            self._date += relativedelta(days=1)
            day_loop += 1


        return daySummaryList
    

    