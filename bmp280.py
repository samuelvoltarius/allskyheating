import board
import busio
import digitalio
import time
import datetime
import ephem
import requests
import adafruit_bmp280
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Define the pins for the relays.
RELAY_1_PIN = 17
RELAY_2_PIN = 27

# Initialize the relays.
relay1 = digitalio.DigitalInOut(board.D17)
relay1.direction = digitalio.Direction.OUTPUT
relay2 = digitalio.DigitalInOut(board.D27)
relay2.direction = digitalio.Direction.OUTPUT

# Create an I2C bus and BMP280 sensor.
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Create a OneWire bus and DS18X20 temperature sensors.
ow_bus = OneWireBus(board.D2)
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

# Your OpenWeatherMap API key and city name
API_KEY = "Your API"
CITY_NAME = "Your City"


def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


# Function to calculate sunrise and sunset times using ephem
def calculate_sun_times():
    observer = ephem.Observer()
    # Enter the coordinates of your location here
    observer.lat = '47.9161'  # Latitude of Seekirchen am Wallersee
    observer.lon = '13.1462'  # Longitude of Seekirchen am Wallersee

    sun = ephem.Sun()
    sunrise = observer.next_rising(sun)
    sunset = observer.next_setting(sun)

    # Sunset + 0.5 hours
    sunrise_time = ephem.localtime(sunrise).strftime('%H:%M:%S')
    sunset_time = (ephem.localtime(sunset) + datetime.timedelta(minutes=30)).strftime('%H:%M:%S')

    return sunrise_time, sunset_time


# Function to write status and sensor info to HTML
def write_status_html(relay1_status, relay2_status, temp1, temp2, bmp_temperature, bmp_pressure, bmp_humidity, sunrise, sunset, snow, forecast, sensor_info):
    color1 = "green" if relay1_status else "red"
    color2 = "green" if relay2_status else "red"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("status.html", "w") as file:
        file.write(f"""
        <html>
        <head><title>Status</title></head>
        <body>
            <p>Status updated at: {timestamp}</p>
            <p>Sunrise: {sunrise}</p>
            <p>Sunset: {sunset}</p>
            <p>Relay 1: <span style="color:{color1};">{relay1_status}</span></p>
            <p>Relay 2: <span style="color:{color2};">{relay2_status}</span></p>
            <p>Temperature 1: {temp1:.2f} °C</p>
            <p>Temperature 2: {temp2:.2f} °C</p>
            <p>BMP280 Temperature: {bmp_temperature:.2f} °C</p>
            <p>BMP280 Pressure: {bmp_pressure:.2f} hPa</p>
            <p>BMP280 Humidity: {bmp_humidity:.2f} %</p>
            <p>Snowfall: {snow}</p>
            <p>Forecast Temperature: {forecast:.2f} °C</p>
            <p>Sensor Info: {sensor_info}</p>
            <form method="post">
                <label>Relay 1: </label>
                <button name="relay1" value="on">On</button>
                <button name="relay1" value="off">Off</button><br>
                <label>Relay 2: </label>
                <button name="relay2" value="on">On</button>
                <button name="relay2" value="off">Off</button>
            </form>
        </body>
        </html>
        """)
