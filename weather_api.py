import requests

def get_weather(city, key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}"
        r = requests.get(url).json()
        temp = r["main"]["temp"]
        desc = r["weather"][0]["description"]
        return f"🌤 Weather in {city}:\nTemp: {temp}°C\nCondition: {desc}"
    except Exception as e:
        return f"Error fetching weather: {e}"
