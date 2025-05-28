import os
import discord
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Alert codes and their descriptions
ALERT_CODES = {
    # Error codes
    "E001": "DHT11 sensor error",
    "E002": "Soil moisture sensor error",
    "E003": "Both sensors failed",
    
    # Status codes
    "S001": "Soil moist enough - No watering needed",
    
    # Alert codes
    "A001": "Mildly dry soil - Short watering",
    "A002": "Dry soil - Medium watering",
    "A003": "Very dry soil - Long watering + alert",
    "A004": "Extreme heat and dryness - Extra watering"
}

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

def get_latest_alert():
    """Fetch the latest alert from the database"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT timestamp, temperature, humidity, soil_moisture, light_level, alert_code
            FROM sensor_data_group_2
            WHERE alert_code IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        
        result = cur.fetchone()
        if result:
            return {
                'timestamp': result[0],
                'temperature': result[1],
                'humidity': result[2],
                'soil_moisture': result[3],
                'light_level': result[4],
                'alert_code': result[5]
            }
        return None
    except Exception as e:
        print(f"Error fetching latest alert: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def create_alert_embed(alert_code, sensor_data):
    """Create a Discord embed for the alert"""
    if alert_code not in ALERT_CODES:
        return None

    # Determine embed color based on alert type
    color = discord.Color.red()  # Default for errors
    if alert_code.startswith('S'):
        color = discord.Color.green()  # Status messages
    elif alert_code.startswith('A'):
        if alert_code in ['A003', 'A004']:
            color = discord.Color.red()  # Critical alerts
        else:
            color = discord.Color.orange()  # Warning alerts

    embed = discord.Embed(
        title="⚠️ Greenhouse Alert",
        description=ALERT_CODES[alert_code],
        color=color,
        timestamp=datetime.now()
    )

    # Add sensor data to the embed
    if sensor_data:
        embed.add_field(
            name="Current Conditions",
            value=f"Temperature: {sensor_data.get('temperature', 'N/A')}°C\n"
                  f"Humidity: {sensor_data.get('humidity', 'N/A')}%\n"
                  f"Soil Moisture: {sensor_data.get('soil_moisture', 'N/A')}%\n"
                  f"Light Level: {sensor_data.get('light_level', 'N/A')} lux",
            inline=False
        )

    # Add alert type indicator
    alert_type = "Error" if alert_code.startswith('E') else "Status" if alert_code.startswith('S') else "Alert"
    embed.set_footer(text=f"Greenhouse Monitoring System • {alert_type}")

    return embed

async def handle_alert(alert_code, sensor_data, channel):
    """Handle alert notification to Discord"""
    if not alert_code or not channel:
        return

    # Create and send the alert embed
    embed = create_alert_embed(alert_code, sensor_data)
    if embed:
        try:
            await channel.send(embed=embed)
            print(f"Alert sent: {alert_code} - {ALERT_CODES[alert_code]}")
        except Exception as e:
            print(f"Error sending alert to Discord: {e}")

async def send_latest_alert(channel):
    """Fetch and send the latest alert from the database"""
    latest_alert = get_latest_alert()
    if latest_alert:
        await handle_alert(
            latest_alert['alert_code'],
            {
                'temperature': latest_alert['temperature'],
                'humidity': latest_alert['humidity'],
                'soil_moisture': latest_alert['soil_moisture'],
                'light_level': latest_alert['light_level']
            },
            channel
        ) 