# Discord-bot-iot

A Discord bot that integrates IoT functionality with weather monitoring capabilities. This bot allows users to control a water pump system and get weather updates through Discord commands.

## Features

- 🌡️ Real-time weather updates
- 💧 Water pump control (ON/OFF)
- 📊 System status monitoring
- 🤖 Simple Discord commands interface

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- OpenWeatherMap API Key
- IoT hardware setup (water pump system)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/discord-bot-iot.git
cd discord-bot-iot
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```
DISCORD_TOKEN=your_discord_bot_token
CITY=your_city_name
WEATHER_API_KEY=your_openweathermap_api_key
```

## Usage

1. Start the bot:

```bash
python main.py
```

2. Available Commands:

- `!status` - Get current sensor data and system status
- `!pump_on` - Activate the water pump
- `!pump_off` - Deactivate the water pump
- `!weather` - Get current weather update
- `!helpme` - Display available commands

## Project Structure

- `main.py` - Bot initialization and configuration
- `bot_commands.py` - Discord bot commands implementation
- `iot_controller.py` - IoT device control functions
- `weather_api.py` - Weather data fetching functionality

## Dependencies

- discord.py - Discord API wrapper
- python-dotenv - Environment variable management
- requests - HTTP library for API calls

## License

This project is licensed under the MIT License - see the LICENSE file for details.
