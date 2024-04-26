class Geolocation:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.state = kwargs.get("state", None)
        self.country = kwargs.get("country", None)
        self.lat = kwargs.get("lat", None)
        self.lon = kwargs.get("lon", None)

class Temperature:
    def __init__(self, **kwargs):
        self.min = kwargs.get("min", None)
        self.max = kwargs.get("max", None)
        self.afternoon = kwargs.get("afternoon", None)
        self.night = kwargs.get("night", None)
        self.evening = kwargs.get("evening", None)
        self.morning = kwargs.get("morning", None)

class DaySummary:
    def __init__(self, **kwargs):
        self.lat = kwargs.get("lat", None)
        self.lon = kwargs.get("lon", None)
        self.tz = kwargs.get("tz", None)
        self.date = kwargs.get("date", None)
        self.units = kwargs.get("units", None)
        
        self.temperature = None
        _temperature = kwargs.get("temperature", None)
        if _temperature is not None:
            self.temperature = Temperature(**_temperature)