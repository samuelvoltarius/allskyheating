import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
import digitalio
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

# Create a OneWire bus and DS18X20 temperature sensors.
ow_bus = OneWireBus(board.D2)

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
def write_status_html(relay1_status, relay2_status, temp1, temp2, sunrise, sunset, snow, forecast, sensor_info):
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

def is_snowing(weather_data):
    weather_conditions = weather_data.get("weather", [])
    for condition in weather_conditions:
        if condition.get("main") == "Snow":
            return True
    return False

def convert_to_datetime(time_string):
    return datetime.datetime.strptime(time_string, '%H:%M:%S')

# Funktion zum Auswerten des Haupt-Loops
def main_loop():
    prev_relay1 = prev_relay2 = None

    while True:
        try:
            temp1, temp2 = ds18.temperature, ds18.temperature
            sensor_missing = False
        except Exception as e:
            temp1 = temp2 = -999
            sensor_missing = str(e)

        sunrise, sunset = calculate_sun_times()
        sunrise_dt = convert_to_datetime(sunrise)
        sunset_dt = convert_to_datetime(sunset)

        current_datetime = datetime.datetime.now()  # Aktuelles datetime.datetime-Objekt
        current_time = current_datetime.time()  # Aktuelle Zeit extrahieren
        weather_data = get_weather()
        print(weather_data)  # Ausgabe der Wetterdaten zur Überprüfung
        snow_status = is_snowing(weather_data)
        forecast_temp = weather_data.get("main", {}).get("temp", 0)  # Vermeidung von KeyError

        if snow_status:
            relay1.value = True
            relay2.value = True
        else:
            temp_difference = abs(temp1 - temp2)

            if sunrise_dt <= current_datetime <= sunrise_dt + datetime.timedelta(hours=1) or sunset_dt <= current_datetime <= sunset_dt + datetime.timedelta(hours=1):
                if temp_difference >= 15:
                   relay1.value = True
                   relay2.value = True
                elif temp_difference >= 10:
                   relay1.value = False
                   relay2.value = True
                elif temp_difference >= 5:
                   relay1.value = True
                   relay2.value = False
                else:
                   relay1.value = False
                   relay2.value = False
            else:
                relay1.value = relay2.value = False

        # Handle relay control via form here

        if relay1.value != prev_relay1 or relay2.value != prev_relay2:
            sensor_info = f"Sensor 1: {temp1:.2f} °C, Sensor 2: {temp2:.2f} °C" if not sensor_missing else f"Sensor missing: {sensor_missing}"
            write_status_html(
                relay1.value, relay2.value, temp1, temp2, sunrise, sunset,
                "Yes" if snow_status else "No", forecast_temp, sensor_info
            )
            prev_relay1, prev_relay2 = relay1.value, relay2.value
#Time for Loop
        time.sleep(300)

# Run the main loop when the script is executed
if __name__ == "__main__":
    main_loop()
