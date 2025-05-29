import random
import requests
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Get the API base URL from environment variable
API_BASE_URL = "https://3099-2405-6e00-28ec-20d5-1156-2234-ae90-cfad.ngrok-free.app"

def get_db_connection():
    """Create a database connection using DATABASE_URL"""
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")
            
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def control_device(device, action):
    """Control a device (pump/fan) with an action (on/off) via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/control/{device}/{action}")
        response.raise_for_status()
        result = response.json()
        print(f"Response from control device: {result}")
        return result
    except Exception as e:
        print(f"Error controlling device: {str(e)}")
        return {"status": "error", "message": str(e)}

def get_status():
    """Get the latest sensor data from the database"""
    conn = get_db_connection()
    if not conn:
        return "❌ Error: Could not connect to database"

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT temperature, humidity, soil_moisture, light_level
            FROM sensor_data_group_2
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        
        result = cur.fetchone()
        if result:
            temp, humidity, moisture, light = result
            return f"🌡 Temp: {temp}°C\n💧 Humidity: {humidity}%\n🌱 Moisture: {moisture}\n💡 Light: {light} lux"
        return "❌ No sensor data available"
    except Exception as e:
        print(f"Error fetching status: {e}")
        return f"❌ Error fetching status: {str(e)}"
    finally:
        cur.close()
        conn.close()
