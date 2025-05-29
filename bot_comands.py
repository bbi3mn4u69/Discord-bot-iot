from discord.ext import commands, tasks
from iot_controller import control_device, get_status
from weather_api import get_weather
import discord
from ai_api import get_ai_response
from ai_frame import ai_frame
from alert_handler import handle_alert, send_latest_alert, get_latest_alert
import os

def setup_bot(bot):
    # Store the last sent alert timestamp and name
    last_alert_timestamp = None
    last_alert_name = None

    @tasks.loop(minutes=5)  # Check every minute
    async def check_new_alerts():
        """Background task to check for new alerts"""
        try:
            # Get the alert channel
            alert_channel_id = int(os.getenv("ALERT_CHANNEL_ID"))
            channel = bot.get_channel(alert_channel_id)
            if not channel:
                print("Alert channel not found")
                return

            # Get the latest alert
            latest_alert = get_latest_alert()
            if not latest_alert:
                return

            nonlocal last_alert_timestamp, last_alert_name
            # If this is a new alert (different timestamp or different alert name), send it
            if (last_alert_timestamp is None or 
                latest_alert['timestamp'] > last_alert_timestamp or 
                latest_alert['alert_code'] != last_alert_name):
                await send_latest_alert(channel)
                last_alert_timestamp = latest_alert['timestamp']
                last_alert_name = latest_alert['alert_code']
                print(f"New alert sent: {latest_alert['alert_code']}")

        except Exception as e:
            print(f"Error in check_new_alerts: {e}")

    @bot.event
    async def on_ready():
        print(f'{bot.user} is online.')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!helpme"))
        # Start the background task when the bot is ready
        check_new_alerts.start()

    @bot.event
    async def on_disconnect():
        # Stop the background task when the bot disconnects
        check_new_alerts.cancel()

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
            response = control_device("pump", "on")
            if response["status"] == "success":
                embed = discord.Embed(
                    title="🚿 Pump Control",
                    description="Water pump has been activated",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Error activating pump: {response['message']}")
        except Exception as e:
            await ctx.send(f"❌ Error activating pump: {str(e)}")

    @bot.command()
    async def pump_off(ctx):
        try:
            response = control_device("pump", "off")
            if response["status"] == "success":
                embed = discord.Embed(
                    title="🚿 Pump Control",
                    description="Water pump has been deactivated",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Error deactivating pump: {response['message']}")
        except Exception as e:
            await ctx.send(f"❌ Error deactivating pump: {str(e)}")

    @bot.command()
    async def weather(ctx):
        try:
            weather_data = get_weather()
            
            # Create the main embed
            embed = discord.Embed(
                title="🌤 Weather Update for Melbourne",
                description=weather_data,
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
            
            
    @bot.command(name='qa')
    async def qa(ctx, *, question: str):
        """
        Ask the AI a question. Everything after !qa is captured as `question`.
        """
        try:
            # pass the user's question to the AI helper
            ai_response = ai_frame(None, question, None)

            # build an embed (or plain text) to send back
            embed = discord.Embed(
                title="🤖 AI Response",
                description=ai_response,
                color=discord.Color.teal()
            )
            embed.add_field(name="Q: ", value=question, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error from AI: {e}")

    @bot.command()
    async def latest_alert(ctx):
        """Fetch and display the latest alert from the database"""
        try:
            await send_latest_alert(ctx.channel)
        except Exception as e:
            await ctx.send(f"❌ Error fetching latest alert: {str(e)}")

    @bot.command()
    async def fan_on(ctx):
        try:
            response = control_device("fan", "on")
            if response["status"] == "success":
                embed = discord.Embed(
                title="🌬️ Fan Control",
                description="Fan has been activated",
                color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Error activating fan: {response['message']}")
        except Exception as e:
            await ctx.send(f"❌ Error activating fan: {str(e)}")

    @bot.command()
    async def fan_off(ctx):
        try:
            response = control_device("fan", "off")
            if response["status"] == "success":
                embed = discord.Embed(
                title="🌬️ Fan Control",
                description="Fan has been deactivated",
                color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Error deactivating fan: {response['message']}")
        except Exception as e:
            await ctx.send(f"❌ Error deactivating fan: {str(e)}")

    @bot.command()
    async def fan_status(ctx):
        try:
            status = get_status()
            embed = discord.Embed(
                title="🌬️ Fan Status",
                description=f"Fan is currently {'ON' if status else 'OFF'}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error getting fan status: {str(e)}")

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
            name="!latest_alert",
            value="Get the most recent alert from the system",
            inline=False
        )
        embed.add_field(
            name="!helpme",
            value="Display this help message",
            inline=False
        )
        embed.add_field(
            name="!ai",
            value="Get AI-powered greenhouse management recommendations",
            inline=False
        )
        embed.add_field(
            name="!fan_on",
            value="Activate the fan",
            inline=False
        )
        embed.add_field(
            name="!fan_off",
            value="Deactivate the fan",
            inline=False
        )
        embed.add_field(
            name="!fan_status",
            value="Get the current status of the fan",
            inline=False
        )
        embed.add_field(
            name="!qa <question>",
            value="Ask the AI a question",
            inline=False
        )
        await ctx.send(embed=embed)
