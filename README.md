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

Adding BMP280 as an Optional Component

To connect the BMP280:

1. Connect the SDA pin of the BMP280 to the SDA pin (Serial Data) of your microcontroller.
2. Connect the SCL pin of the BMP280 to the SCL pin (Serial Clock) of your microcontroller.
3. Connect the VCC pin of the BMP280 to the supply voltage (3.3V or 5V) of your microcontroller.
4. Connect the GND pin of the BMP280 to the ground (GND) of your microcontroller.

Please ensure correct pin connections and voltage compatibility. If using a different microcontroller, refer to its I2C connection pins and manufacturer instructions.

The BMP280 can be integrated as an additional option within your existing setup.




## Setting Up as a Systemd Service




To set up the script as a systemd service, follow these steps:


1. Create a new systemd service unit file for your script:



sudo nano /etc/systemd/system/your-script.service

Replace your-script with a suitable name for your service.



2. Add the following content to the your-script.service file:

[Unit]

Description=Your Python Script Autostart

After=multi-user.target

[Service]

ExecStart=/usr/bin/python3 /path/to/your/main.py

WorkingDirectory=/path/to/your/script/directory

StandardOutput=inherit

StandardError=inherit

Restart=always

User=pi  # Change this to your username if not using "pi"

[Install]

WantedBy=multi-user.target


Replace /path/to/your/main.py and /path/to/your/script/directory with the actual paths.




Enable the systemd service:

3. sudo systemctl enable your-script.service



Start the service to ensure it's working:

4. sudo systemctl start your-script.service



Check the status of the service with:

5. sudo systemctl status your-script.service




Contributing



Contributions are welcome! Please fork this repository and submit a pull request.
