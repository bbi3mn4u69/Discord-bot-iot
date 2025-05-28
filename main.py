import os
import discord
from discord.ext import commands
from bot_comands import setup_bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents,)

setup_bot(bot)

bot.run(TOKEN)
