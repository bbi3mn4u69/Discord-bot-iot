from discord.ext import commands
from iot_controller import turn_on_pump, turn_off_pump, get_status
from weather_api import get_weather
import discord

def setup_bot(bot, city, weather_key):
    @bot.event
    async def on_ready():
        print(f'{bot.user} is online.')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!helpme"))

    @bot.command()
    async def status(ctx):
        try:
            status_data = get_status()
            embed = discord.Embed(
                title="🌱 System Status",
                description=status_data,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error getting status: {str(e)}")

    @bot.command()
    async def pump_on(ctx):
        try:
            turn_on_pump()
            embed = discord.Embed(
                title="🚿 Pump Control",
                description="Water pump has been activated",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error activating pump: {str(e)}")

    @bot.command()
    async def pump_off(ctx):
        try:
            turn_off_pump()
            embed = discord.Embed(
                title="💧 Pump Control",
                description="Water pump has been deactivated",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error deactivating pump: {str(e)}")

    @bot.command()
    async def weather(ctx):
        try:
            weather_data = get_weather(city, weather_key)
            embed = discord.Embed(
                title="🌤 Weather Update",
                description=weather_data,
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error getting weather: {str(e)}")

    @bot.command()
    async def helpme(ctx):
        embed = discord.Embed(
            title="🤖 Bot Commands",
            description="Here are all the available commands:",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="!status",
            value="Get current sensor data and system status",
            inline=False
        )
        embed.add_field(
            name="!pump_on",
            value="Activate the water pump",
            inline=False
        )
        embed.add_field(
            name="!pump_off",
            value="Deactivate the water pump",
            inline=False
        )
        embed.add_field(
            name="!weather",
            value="Get current weather update for your city",
            inline=False
        )
        embed.add_field(
            name="!helpme",
            value="Display this help message",
            inline=False
        )
        await ctx.send(embed=embed)
