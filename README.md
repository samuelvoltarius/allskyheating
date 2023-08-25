# allskyheating

	•	DS18B20 Temperature Sensors:
	•	Connect the data pin of each DS18B20 sensor to the D2 pin of the board.
	•	Relays:
	•	Connect the control pin of Relay 1 to the D17 pin of the board.
	•	Connect the control pin of Relay 2 to the D27 pin of the board.
	•	OneWire Bus:
	•	Connect the data pin of the OneWire bus to the D2 pin of the board.
	•	
Please make sure to double-check the connections and ensure that they match the ones mentioned in the code.


	1	Install the required Python modules. You can do this with the following command:
 
pip3 install board busio digitalio adafruit_ds18b20 time datetime ephem requests

	2	Create a file named main.py and paste the code from the question.
	3	Connect the DS18B20 sensors and relays to your Raspberry Pi. The pinout for the sensors and relays is specified in the main.py file.
	4	Run the code with the following command: python3 main.py

The code should now control the relays based on the current conditions. You can check the current status of the relays and temperature in the HTML file status.html.
Here are some tips for testing the code:

	•	Make sure the DS18B20 sensors are connected correctly.
	•	Make sure the relays are connected correctly.
	•	Check that the settings in the main.py file are suitable for your location and needs.
Here are some additional details about each step:

This Python script uses the Adafruit CircuitPython library to control relays based on temperature differences and time of day. It also fetches weather information from the OpenWeatherMap API to determine if it's snowing. The script calculates sunrise and sunset times using the ephem library based on location coordinates. The status of the relays, temperatures, sunrise, sunset, snowfall, and a manual control form are displayed in an HTML file, which is updated regularly.
Key features of the code:

	•	Relays are controlled based on temperature differences and time of day.
	•	Weather information is fetched from the OpenWeatherMap API to check for snowfall.
	•	Sunrise and sunset times are calculated using the ephem library and location coordinates.
	•	The script generates an HTML file displaying relay statuses, temperatures, sunrise, sunset, and snowfall.
	•	The HTML page includes buttons to manually control the relays.
	•	The code can be modified and executed directly to operate the relays and monitor the weather.


 Create a systemd Service:
Open a terminal and create a new systemd service unit file for your script:
bash
Copy code
sudo nano /etc/systemd/system/your-script.service
Replace your-script with a suitable name for your service.
Add the Service Configuration:
Add the following content to the your-script.service file:
plaintext
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
Make sure to replace /path/to/your/main.py and /path/to/your/script/directory with the actual paths.
Enable the Service:
Enable the systemd service you just created:
bash
Copy code
sudo systemctl enable your-script.service
Start the Service:
Start the service to ensure it's working:
bash
Copy code
sudo systemctl start your-script.service
Reboot and Test:
Reboot your Raspberry Pi:
bash
Copy code
sudo reboot
Your Python script should now start automatically after the reboot. You can check the status of the service with:
bash
Copy code
sudo systemctl status your-script.service
Feel free to modify the code to suit your specific needs, such as adjusting the location coordinates, API key, and other parameters.
