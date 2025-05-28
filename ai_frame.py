import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def format_weather_data(weather_data):
    if weather_data is None:
        return None
        
    # Get current conditions
    current = weather_data.iloc[0]
    temp_min = weather_data['temperature_2m'].min()
    temp_max = weather_data['temperature_2m'].max()
    temp_current = current['temperature_2m']
    wind_current = current['wind_speed_10m']
    wind_max = weather_data['wind_speed_10m'].max()
    sunshine_total = weather_data['sunshine_duration'].sum() / 3600  # Convert to hours
    
    # Format the weather data into a readable string
    weather_summary = f"""
Weather Data for {current['date'].strftime('%Y-%m-%d')}:
Location: Melbourne, Australia
Coordinates: -37.75°N, 144.875°E
Elevation: 19.0m

Current Conditions:
- Temperature: {temp_current:.1f}°C (Min: {temp_min:.1f}°C, Max: {temp_max:.1f}°C)
- Wind Speed: {wind_current:.1f} km/h (Max: {wind_max:.1f} km/h)
- Total Sunshine: {sunshine_total:.1f} hours

Hourly Forecast:
"""
    
    # Add hourly data
    for _, row in weather_data.iterrows():
        time = row['date'].strftime('%H:%M')
        temp = row['temperature_2m']
        wind = row['wind_speed_10m']
        sun = row['sunshine_duration'] / 3600
        weather_summary += f"{time}: Temp {temp:.1f}°C, Wind {wind:.1f} km/h, Sun {sun:.1f}h\n"
    
    return weather_summary

def ai_frame(system_message, message, weather_data):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        contents = []
        
        if system_message:
            contents.append(genai.types.Part(text=system_message))
        if message:
            contents.append(genai.types.Part(text=message))
        if weather_data is not None:
            formatted_weather = format_weather_data(weather_data)
            contents.append(genai.types.Part(text=formatted_weather))
            
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )    
        return response.text
    except Exception as e:
        return f"Error fetching AI response in ai_frame: {e}"





