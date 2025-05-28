import os
from google import genai
from dotenv import load_dotenv
from weather_api import get_weather
from ai_frame import ai_frame

load_dotenv()

SYSTEM_MESSAGE = "You are a helpful assistant that can give recommendation based on the weather data. You are created by Bill Pham and Anthony, you will help the farmer of the greenhouse to determine if that's neceessary to turn on the water pump. based on the weather forcast with the temperature and give the farmer a recommendation and the reason to turn on the water pump and the green house fan or not. The weather loacation is in melbourne, australia. Please only give the recommendation do not hallucinate or make up any information."

def get_ai_response():
    try:
        weather_data = get_weather()
        ai_response = ai_frame(SYSTEM_MESSAGE, None, weather_data) 
        print(ai_response)
        return ai_response
    except Exception as e:
        return f"Error fetching AI response: {e}"





