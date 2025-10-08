import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> str:
    """Gets the current weather for a given city from an API."""
    if not API_KEY:
        return "Error: Weather API key is not configured."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The current weather in {city} is {temp}°C with {weather_desc}."
    except Exception as e:
        return f"Sorry, an error occurred while fetching the weather: {e}"