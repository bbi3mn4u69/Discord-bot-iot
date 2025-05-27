from discord.ext import commands
from iot_controller import turn_on_pump, turn_off_pump, get_status
from weather_api import get_weather

def setup_bot(bot, city, weather_key):
    @bot.event
    async def on_ready():
        print(f'{bot.user} is online.')

    @bot.command()
    async def status(ctx):
        await ctx.send(get_status())

    @bot.command()
    async def pump_on(ctx):
        turn_on_pump()
        await ctx.send("🚿 Pump ON")

    @bot.command()
    async def pump_off(ctx):
        turn_off_pump()
        await ctx.send("💧 Pump OFF")

    @bot.command()
    async def weather(ctx):
        await ctx.send(get_weather(city, weather_key))

    @bot.command()
    async def helpme(ctx):
        await ctx.send("""
🤖 Commands:
!status - Sensor data
!pump_on - Activate pump
!pump_off - Deactivate pump
!weather - Weather update
""")
