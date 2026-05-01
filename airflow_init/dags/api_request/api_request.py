import requests
import pprint
   
api_key = "5f232438ab0238f052d406754aa1c0b9"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"

def featch_data() -> dict :
    """
    Fetch current weather data from Weatherstack API.

    This function sends a GET request to the Weatherstack API using the
    provided API key and query location. It validates
    the response, prints status messages, and returns the weather data
    as a Python dictionary.

    Returns:
        dict: JSON response containing weather information such as
              location details and current weather conditions.

    Raises:
        requests.exceptions.RequestException: If the API request fails
        due to network issues, invalid API key, or incorrect parameters.
    """

    print("Featching Weather data from weatherstack.com......")

    try :
        responce = requests.get(api_url)
        responce.raise_for_status()

        print("API responce recived successfully ^_^ ")
        return responce.json()

    except requests.exceptions.RequestException as e :
        print(f"error occurred  ^.^ : {e}")
        raise


def mock_fetch_data() -> dict :
    return {'request': {'type': 'City',
             'query': 'New York, United States of America',
             'language': 'en',
             'unit': 'm'},
 'location': {'name': 'New York',
              'country': 'United States of America',
              'region': 'New York',
              'lat': '40.714',
              'lon': '-74.006',
              'timezone_id': 'America/New_York',
              'localtime': '2026-04-22 23:14',
              'localtime_epoch': 1776899640,
              'utc_offset': '-4.0'},
 'current': {'observation_time': '03:14 AM',
             'temperature': 10,
             'weather_code': 122,
             'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'],
             'weather_descriptions': ['Overcast'],
             'astro': {'sunrise': '06:07 AM',
                       'sunset': '07:43 PM',
                       'moonrise': '10:07 AM',
                       'moonset': '01:14 AM',
                       'moon_phase': 'Waxing Crescent',
                       'moon_illumination': 27},
             'air_quality': {'co': '355.85',
                             'no2': '80.25',
                             'o3': '4',
                             'so2': '10.05',
                             'pm2_5': '30.85',
                             'pm10': '32.95',
                             'us-epa-index': '2',
                             'gb-defra-index': '2'},
             'wind_speed': 6,
             'wind_degree': 47,
             'wind_dir': 'NE',
             'pressure': 1016,
             'precip': 0,
             'humidity': 74,
             'cloudcover': 100,
             'feelslike': 10,
             'uv_index': 0,
             'visibility': 16,
             'is_day': 'no'}}