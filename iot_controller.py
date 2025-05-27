import random
# try:
#     import RPi.GPIO as GPIO
#     PUMP_PIN = 18
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(PUMP_PIN, GPIO.OUT)
# except:
#     print("GPIO not available, running in debug mode.")

def turn_on_pump():
    
    try:
        print("Pump ON (simulated)")
        # GPIO.output(PUMP_PIN, GPIO.HIGH)
    except:
        pass

def turn_off_pump():
    
    try:
        print("Pump OFF (simulated)")
        # GPIO.output(PUMP_PIN, GPIO.LOW)
    except:
        pass

def get_status():
    temp = round(random.uniform(24.0, 32.0), 1)
    moisture = random.randint(300, 800)
    return f"🌡 Temp: {temp}°C\n🌱 Moisture: {moisture}"
