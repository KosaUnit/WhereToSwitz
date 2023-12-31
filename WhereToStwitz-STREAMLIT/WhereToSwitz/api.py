import requests
import config
import pandas as pd
import streamlit as st
from datetime import datetime

canton_capital_dict = {
    "Aargau": "Aarau",
    "Appenzell Ausserrhoden": "Herisau",
    "Appenzell Innerrhoden": "Appenzell",
    "Basel-Landschaft": "Liestal",
    "Basel-Stadt": "Basel",
    "Bern": "Bern",
    "Fribourg": "Fribourg",
    "Geneva": "Geneva",
    "Glarus": "Glarus",
    "Graubünden": "Chur",
    "Jura": "Delémont",
    "Lucerne": "Lucerne",
    "Neuchâtel": "Neuchâtel",
    "Nidwalden": "Stans",
    "Obwalden": "Sarnen",
    "Schaffhausen": "Schaffhausen",
    "Schwyz": "Schwyz",
    "Solothurn": "Solothurn",
    "St. Gallen": "St. Gallen",
    "Thurgau": "Frauenfeld",
    "Ticino": "Bellinzona",
    "Uri": "Altdorf",
    "Valais": "Sion",
    "Vaud": "Lausanne",
    "Zug": "Zug",
    "Zurich": "Zurich"
}

cantonal_data_dict = { 'Canton': [],
                        'City': [],
                        'Temperature': [],
                        'Weather': [],
                        'Distinct weather': [],
                        'Icon': []
                        }

def update_cantonal_data_dict(dict: dict, canton_name: str, city_name: str, temp: str, weather: str, distinct_weather: str, icon: str) -> None:
    """
    Updates a dictionary containing cantonal weather data with new information.

    This function appends data for a specific canton to the provided dictionary.

    Parameters:
    - data_dict (dict): The dictionary containing cantonal weather data.
    - canton_name (str): The name of the canton.
    - city_name (str): The name of the city in the canton.
    - temp (str): The temperature in the city.
    - weather (str): The general weather condition.
    - distinct_weather (str): A distinct weather description.
    - icon (str): The icon representing the weather.

    Returns:
    - None: The function modifies the provided dictionary in place.

    Note:
    The function appends data to the specified dictionary. Make sure to initialize the dictionary appropriately before using this function.
    """
    dict['Canton'].append(canton_name)
    dict['City'].append(city_name)
    dict['Temperature'].append(temp)
    dict['Weather'].append(weather)
    dict['Distinct weather'].append(distinct_weather)
    dict['Icon'].append(icon)

@st.cache_data(ttl=10800)
def fetch_cantonal_data_from_api() -> pd.DataFrame:
    '''
    Add 
    '''
    for key, val in canton_capital_dict.items():
        canton_name = key
        city_name = val
        limit = 1
        loc_api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={config.API_key}'
        loc_api_response = requests.get(loc_api_url)
        lat = loc_api_response.json()[0]['lat']
        lon = loc_api_response.json()[0]['lon'] 
        weather_api = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.API_key}&units=metric'
        weather_api_response = requests.get(weather_api)
        temp = weather_api_response.json()['main']['temp']
        weather = weather_api_response.json()['weather'][0]['main']
        distinct_weather = weather_api_response.json()['weather'][0]['description']
        icon = weather_api_response.json()['weather'][0]['icon'] 
        icon_URL = f'https://openweathermap.org/img/wn/{icon}@2x.png'
        # TO DO: Consider if icon information may increase a fetching data time -> if it does use different solution 
        print(icon_URL)
        icon_response = requests.get(icon_URL)
        if icon_response.status_code == 200:
            icon_data = icon_response.content
        else:
            print(f"Failed to fetch icon. Status code: {icon_response.status_code}")

        # TO DO - Confirm that is switz town 
        update_cantonal_data_dict(cantonal_data_dict, canton_name, city_name, temp, weather, distinct_weather, icon_URL)

        # print(cantonal_data_dict)
        # # Temporary 
        # break
    return pd.DataFrame(cantonal_data_dict)





# api delivery - https://openweathermap.org
# Start work on a different branch
# READ IT https://www.dataquest.io/blog/python-api-tutorial/
   