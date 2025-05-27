import os
import discord
from discord.ext import commands
from bot_comands import setup_bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CITY = os.getenv("CITY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents,)

setup_bot(bot, CITY, WEATHER_API_KEY)

bot.run(TOKEN)
