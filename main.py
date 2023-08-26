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

# Function to run the main loop
def main_loop():
    prev_relay1 = prev_relay2 = None

    while True:
        try:
            temp1, temp2 = sensor1.temperature, sensor2.temperature
            sensor_missing = False
        except Exception as e:
            temp1 = temp2 = -999
            sensor_missing = str(e)

        sunrise, sunset = calculate_sun_times()

        current_time = datetime.datetime.now().time()

        if datetime.datetime.strptime(sunset, '%H:%M:%S') <= current_time <= datetime.datetime.strptime(sunrise, '%H:%M:%S') + datetime.timedelta(hours=1):
            weather_data = get_weather()
            snow_status = is_snowing(weather_data)
            forecast_temp = weather_data["main"]["temp"]

            relay1.value = relay2.value = snow_status or (temp1 - temp2 >= 15) or (temp1 - temp2 >= 10)

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

        time.sleep(1)

# Run the main loop when the script is executed
if __name__ == "__main__":
    main_loop()
