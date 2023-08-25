import board
import busio
import digitalio
import adafruit_ds18b20
import time
import datetime
import ephem
import requests

# Define the pins for the relays.
RELAY_1_PIN = 17
RELAY_2_PIN = 27

# Initialize the relays.
relay1 = digitalio.DigitalInOut(board.D17)
relay1.direction = digitalio.Direction.OUTPUT
relay2 = digitalio.DigitalInOut(board.D27)
relay2.direction = digitalio.Direction.OUTPUT

# Create a OneWire bus.
bus = busio.OneWire(board.D2)

# Create two DS18B20 temperature sensors.
sensor1 = adafruit_ds18b20.DS18B20(bus)
sensor2 = adafruit_ds18b20.DS18B20(bus)

# Your OpenWeatherMap API key and city name
API_KEY = "YOUR_API_KEY"
CITY_NAME = "Seekirchen am Wallersee"

# Function to write relay status, temperature, and weather to an HTML file
def write_status_html(relay1_status, relay2_status, temperature1, temperature2, sunrise_time, sunset_time, snow_status, forecast_temp):
    color1 = "green" if relay1_status else "red"
    color2 = "green" if relay2_status else "red"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("status.html", "w") as file:
        file.write(f"""
        <html>
        <head>
            <title>Status</title>
        </head>
        <body>
            <p>Status updated at: {timestamp}</p>
            <p>Sunrise: {sunrise_time}</p>
            <p>Sunset: {sunset_time}</p>
            <p>Relay 1: <span style="color:{color1};">{relay1_status}</span></p>
            <p>Relay 2: <span style="color:{color2};">{relay2_status}</span></p>
            <p>Temperature 1: {temperature1:.2f} °C</p>
            <p>Temperature 2: {temperature2:.2f} °C</p>
            <p>Snowfall: {snow_status}</p>
            <p>Forecast Temperature: {forecast_temp:.2f} °C</p>
            <form method="post">
                <label>Relay 1: </label>
                <button name="relay1" value="on">On</button>
                <button name="relay1" value="off">Off</button>
                <br>
                <label>Relay 2: </label>
                <button name="relay2" value="on">On</button>
                <button name="relay2" value="off">Off</button>
            </form>
        </body>
        </html>
        """)

# Function to calculate sunrise and sunset times
def calculate_sun_times():
    observer = ephem.Observer()
    # You can enter the coordinates of your location here
    observer.lat = '47.9161'  # Latitude of Seekirchen am Wallersee
    observer.lon = '13.1462'  # Longitude of Seekirchen am Wallersee
    
    sun = ephem.Sun()
    sunrise = observer.next_rising(sun)
    sunset = observer.next_setting(sun)
    
    # Sunset + 0.5 hours
    sunrise_time = ephem.localtime(sunrise).strftime('%H:%M:%S')
    sunset_time = (ephem.localtime(sunset) + datetime.timedelta(minutes=30)).strftime('%H:%M:%S')
    
    return sunrise_time, sunset_time

# Function to fetch current weather data
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

# Function to check if it's snowing
def is_snowing(weather_data):
    if "weather" in weather_data and len(weather_data["weather"]) > 0:
        main_weather = weather_data["weather"][0]["main"].lower()
        return "snow" in main_weather
    return False

# Function to run the main loop
def main_loop():
    prev_relay1_status = None
    prev_relay2_status = None

    while True:
        temperature1 = sensor1.temperature
        temperature2 = sensor2.temperature

        sunrise_time, sunset_time = calculate_sun_times()

        current_time = datetime.datetime.now().time()

        if datetime.datetime.strptime(sunset_time, '%H:%M:%S') <= current_time <= datetime.datetime.strptime(sunrise_time, '%H:%M:%S') + datetime.timedelta(hours=1):
            weather_data = get_weather()
            snow_status = is_snowing(weather_data)
            forecast = weather_data["main"]["temp"]

            if snow_status:
                relay1.value = True
                relay2.value = True
            elif temperature1 - temperature2 >= 15:
                relay1.value = True
                relay2.value = True
            elif temperature1 - temperature2 >= 10:
                relay1.value = True
                relay2.value = False
            elif temperature1 - temperature2 >= 5:
                relay1.value = False
                relay2.value = True
            else:
                relay1.value = False
                relay2.value = False
        else:
            relay1.value = False
            relay2.value = False

        # Add your code here to handle relay control via the form

        if relay1.value != prev_relay1_status or relay2.value != prev_relay2_status:
            write_status_html(relay1.value, relay2.value, temperature1, temperature2, sunrise_time, sunset_time, "Yes" if snow_status else "No", forecast)
            prev_relay1_status = relay1.value
            prev_relay2_status = relay2.value

        time.sleep(1)
