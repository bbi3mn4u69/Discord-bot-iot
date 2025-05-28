import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def ai_frame(system_message, message, weather_data):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        contents = []
        if system_message:
            contents.append(genai.types.Part(text=system_message))
        if message:
            contents.append(genai.types.Part(text=message))
        if weather_data:
                contents.append(genai.types.Part(text=str(weather_data)))
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )    
        print(response.text)
        return response.text
    except Exception as e:
        return f"Error fetching AI response: {e}"





