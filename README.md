AllSkyHeating
This repository contains a Python script that controls relays based on temperature, time of day, and weather conditions. It calculates sunrise and sunset times using the ephem library and displays relay status, temperatures, sunrise, sunset, and snowfall in an HTML file. The HTML page also allows manual relay control.

Requirements
Raspberry Pi
Python 3
CircuitPython libraries
DS18B20 temperature sensors
Relays
OneWire bus
Installation
Install the required Python modules:

1. pip3 install board busio digitalio adafruit_ds18b20 time datetime ephem requests
2. Create a file named `main.py` and paste the code from this repository.
3. Connect the DS18B20 sensors and relays to your Raspberry Pi based on the specified pinout.
4. Run the code using the command:

python3 main.py

Usage
The code will control the relays based on the conditions and update the status in the status.html file. 
To view the status, open the status.html file in a web browser.

Configuration
The following settings can be configured in the main.py file:


1. location: The latitude and longitude of your location.
2. api_key: Your API key from OpenWeatherMap.
3. relay_1_pin: The GPIO pin for Relay 1.
4. relay_2_pin: The GPIO pin for Relay 2.

Contributing

Contributions are welcome! Please fork this repository and submit a pull request.
