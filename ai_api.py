import os
from google import genai
from dotenv import load_dotenv
from weather_api import get_weather

load_dotenv()

SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks. You are created by Bill Pham and Anthony, you will help the farmer of the greenhouse to determine if that's neceessary to turn on the water pump. based on the weather forcast with the temperature and give the farmer a recommendation and the reason to turn on the water pump and the green house fan or not. The weather loacation is in melbourne, australia."

def get_ai_response():
    try:
        weather_data = get_weather()
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=[
                genai.types.Part(text=SYSTEM_MESSAGE),
                genai.types.Part(text=str(weather_data))
            ]
        )
        print(weather_data)
        print(type(weather_data))
        
        print(response.text)
        return response.text
    except Exception as e:
        return f"Error fetching AI response: {e}"





