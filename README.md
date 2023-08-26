AllSkyHeating

DS18B20 Temperature Sensors:

Connect the data pin of each DS18B20 sensor to the D2 pin of the board.
Relays:

Connect the control pin of Relay 1 to the D17 pin of the board.
Connect the control pin of Relay 2 to the D27 pin of the board.
OneWire Bus:

Connect the data pin of the OneWire bus to the D2 pin of the board.
Please make sure to double-check the connections and ensure that they match the ones mentioned in the code.

Steps to Run

Install the required Python modules using the following command:
css
Copy code
pip3 install board busio digitalio adafruit_ds18b20 time datetime ephem requests
Create a file named main.py and paste the code from the question.
Connect the DS18B20 sensors and relays to your Raspberry Pi based on the specified pinout.
Run the code using the command: python3 main.py
The code will control the relays based on the conditions and update the status in the status.html file. Here are some tips for testing:

Verify DS18B20 sensor connections.
Verify relay connections.
Check and adjust settings in the main.py file to match your location.
This Python script uses CircuitPython libraries to control relays based on temperature, time of day, and weather conditions. It calculates sunrise and sunset times using the ephem library and displays relay status, temperatures, sunrise, sunset, and snowfall in an HTML file. The HTML page also allows manual relay control.

Create a systemd Service

Create a new systemd service unit file for your script:
bash
Copy code
sudo nano /etc/systemd/system/your-script.service
Replace your-script with a suitable name for your service.
Add the following content to the your-script.service file:
makefile
Copy code
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
Replace /path/to/your/main.py and /path/to/your/script/directory with actual paths.
Enable the systemd service:
bash
Copy code
sudo systemctl enable your-script.service
Start the service to ensure it's working:
sql
Copy code
sudo systemctl start your-script.service
Reboot your Raspberry Pi:
Copy code
sudo reboot
Check the status of the service with:
lua
Copy code
sudo systemctl status your-script.service
Feel free to modify the code to suit your needs, such as location coordinates and API key.

Connecting BMP280 to Microcontroller

Here's how to connect the BMP280 to a microcontroller:

Connect the SDA pin of the BMP280 to the SDA pin (Serial Data) of your microcontroller.
Connect the SCL pin of the BMP280 to the SCL pin (Serial Clock) of your microcontroller.
Connect the VCC pin of the BMP280 to the supply voltage (3.3V or 5V) of your microcontroller.
Connect the GND pin of the BMP280 to the ground (GND) of your microcontroller.
Ensure correct pins and voltage compatibility. If using a different microcontroller, refer to its I2C connection pins and manufacturer instructions.
