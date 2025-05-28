from discord.ext import commands
from iot_controller import turn_on_pump, turn_off_pump, get_status
from weather_api import get_weather
import discord
from ai_api import get_ai_response

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
            weather_data = get_weather()
            
            # Create the main embed
            embed = discord.Embed(
                title="🌤 Weather Update for Melbourne",
                color=discord.Color.orange()
            )
            
            # Get current hour's data (first row)
            current = weather_data.iloc[0]
            
            # Add current conditions
            embed.add_field(
                name="📍 Location",
                value=f"Coordinates: {weather_data.iloc[0]['date'].strftime('%Y-%m-%d')}\nLatitude: -37.75°N\nLongitude: 144.875°E\nElevation: 19.0m",
                inline=False
            )
            
            # Add temperature information
            temp_min = weather_data['temperature_2m'].min()
            temp_max = weather_data['temperature_2m'].max()
            temp_current = current['temperature_2m']
            embed.add_field(
                name="🌡️ Temperature",
                value=f"Current: {temp_current:.1f}°C\nMin: {temp_min:.1f}°C\nMax: {temp_max:.1f}°C",
                inline=True
            )
            
            # Add wind information
            wind_current = current['wind_speed_10m']
            wind_max = weather_data['wind_speed_10m'].max()
            embed.add_field(
                name="💨 Wind",
                value=f"Current: {wind_current:.1f} km/h\nMax: {wind_max:.1f} km/h",
                inline=True
            )
            
            # Add sunshine information
            sunshine_total = weather_data['sunshine_duration'].sum() / 3600  # Convert to hours
            embed.add_field(
                name="☀️ Sunshine",
                value=f"Total: {sunshine_total:.1f} hours",
                inline=True
            )
            
            # Add hourly forecast
            hourly_forecast = "```\nTime    Temp    Wind    Sun\n"
            for _, row in weather_data.iterrows():
                time = row['date'].strftime('%H:%M')
                temp = row['temperature_2m']
                wind = row['wind_speed_10m']
                sun = row['sunshine_duration'] / 3600  # Convert to hours
                hourly_forecast += f"{time}  {temp:6.1f}°C  {wind:6.1f}km/h  {sun:4.1f}h\n"
            hourly_forecast += "```"
            
            embed.add_field(
                name="📅 Hourly Forecast",
                value=hourly_forecast,
                inline=False
            )
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error getting weather: {str(e)}")
    
    @bot.command()
    async def ai(ctx):
        try:
            ai_response = get_ai_response()
            
            # Split the response into sections
            sections = ai_response.split('\n\n')
            
            # Create the main embed
            embed = discord.Embed(
                title="🌱 Greenhouse Management Recommendation",
                color=discord.Color.green()
            )
            
            # Process each section
            for section in sections:
                if section.startswith('**Recommendation:**'):
                    # Extract recommendations
                    recommendations = section.split('*')[1:]
                    for rec in recommendations:
                        if rec.strip():
                            embed.add_field(
                                name="💡 Recommendation",
                                value=rec.strip(),
                                inline=False
                            )
                elif section.startswith('**Reasoning:**'):
                    # Extract reasoning
                    reasons = section.split('*')[1:]
                    for reason in reasons:
                        if reason.strip():
                            embed.add_field(
                                name="📊 Reasoning",
                                value=reason.strip(),
                                inline=False
                            )
                elif section.startswith('**Important Considerations:**'):
                    # Extract considerations
                    considerations = section.split('*')[1:]
                    for consideration in considerations:
                        if consideration.strip():
                            embed.add_field(
                                name="⚠️ Important Consideration",
                                value=consideration.strip(),
                                inline=False
                            )
                elif section.startswith('**Disclaimer:**'):
                    embed.add_field(
                        name="ℹ️ Disclaimer",
                        value=section.replace('**Disclaimer:**', '').strip(),
                        inline=False
                    )
                else:
                    # Handle regular text sections
                    if section.strip():
                        embed.add_field(
                            name="📝 Information",
                            value=section.strip(),
                            inline=False
                        )
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error getting AI response: {str(e)}")

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
