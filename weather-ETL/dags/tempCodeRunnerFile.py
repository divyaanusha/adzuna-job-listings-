import datetime
import requests

def fetch_weather_data():
    print('starttttttttt')
    url = "https://meteostat.p.rapidapi.com/stations/daily"
    querystring = {"station": "10637", "start": "2020-01-01", "end": "2020-01-31"}
    headers = {
        "x-rapidapi-key": "96335aecb2msh29054a09e0eafcdp11f5bbjsnbfe0d23a6dde",
        "x-rapidapi-host": "meteostat.p.rapidapi.com"
    }
    print('hellowwwwwwwwwwwwwwwww')
    response = requests.get(url, headers=headers, params=querystring)
    print('hellowwwwwwwwwwwwwwwww',response.json())
