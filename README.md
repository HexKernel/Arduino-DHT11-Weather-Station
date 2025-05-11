# Advanced-Arduino-Weather-Station-Using-DHT11-and-Serial-Data-Logging

This project utilizes an **Arduino Uno CH340G development board** paired with a **DHT11** temperature and humidity sensor to create a compact yet capable environmental monitoring system. It measures ambient temperature (°C) and relative humidity (%), and based on these, calculates a comprehensive set of derived atmospheric metrics including: Heat Index, Dew Point, Absolute Humidity, Specific Humidity, Mixing Ratio, Vapor Pressure, Saturation Vapor Pressure, Wet Bulb Temperature, Humidex, and Enthalpy.


The main.cpp sketch located in the src directory of this repository consists of a C++ program that begins by importing the DHT.h library, as included in the platformio.ini config. After defining the sensor type and the corresponding data pin, the sketch initializes serial communication at a 9600 baud rate. A short delay follows to allow the DHT11 sensor to stabilize before data collection begins.

Within the loop() function, the program attempts to read temperature and humidity values from the sensor. If either value is invalid (NaN), the system prints a row of "nan" values and waits one second before retrying. When valid data is received, the program proceeds to calculate multiple atmospheric parameters based on the raw sensor input.

Before transmitting the results to the serial monitor, the program calls a function that blinks the onboard LED three times, visually signaling that the data was successfully retrieved from the DHT11 module. The calculated values are then output in comma-separated format at two-second intervals, providing a continuous stream of real-time environmental data.


