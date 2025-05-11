# Advanced-Arduino-Weather-Station-Using-DHT11-and-Serial-Data-Logging

This project utilizes an **Arduino Uno CH340G development board** paired with a **DHT11** temperature and humidity sensor to create a compact yet capable environmental monitoring system. It measures **ambient temperature (°C)** and **relative humidity (%)**, and based on these, calculates a comprehensive set of derived atmospheric metrics including: Heat Index, Dew Point, Absolute Humidity, Specific Humidity, Mixing Ratio, Vapor Pressure, Saturation Vapor Pressure, Wet Bulb Temperature, Humidex, and Enthalpy.

<p align="center">
  <img src="assets/img 1 - Arduino Uno CH340G.jpeg" width="28%">
  <img src="assets/img 2 - DHT11 Module.jpeg" width="17.79%">
  <img src="assets/img 3 - Setup.jpeg" width="40%">
</p>

The ```main.cpp``` sketch located in the ```/src``` directory of this repository consists of a C++ program that begins by importing the ```DHT.h``` library, as included in the ```platformio.ini``` config. After defining the sensor type and the corresponding data pin, the sketch initializes serial communication at a **9600 baud rate**. A short delay follows to allow the DHT11 sensor to stabilize before data collection begins. Within the ```loop()``` function, the program attempts to read temperature and humidity values from the sensor. If either value is **invalid (NaN)**, the system prints a row of **"nan"** values and waits one second before retrying. 

When valid data is received, the program proceeds to calculate multiple atmospheric parameters based on the raw sensor input. Before transmitting the results to the serial monitor, the program calls a function that blinks the onboard LED three times, visually signaling that the data was successfully retrieved from the DHT11 module. The calculated values are then output in comma-separated format at two-second intervals, providing a continuous stream of real-time environmental data.

### Example Output

```bash
27.00,43.00,27.02,15.60,11.04,0.21102,0.27,15.29,35.57,18.54,29.94,1124.19
nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
```  

Each row represents a full sensor readout and computed atmospheric metrics, output every 2 seconds:

| Description                          | Temp (°C) | RH (%) | Heat Index (°C)             | Dew Point (°C)                  | Abs. Humidity (g/m³)                                               | Spec. Humidity              | Mix. Ratio (g/kg)                         | Vapor Pressure (hPa)                                         | Sat. Vap. Pressure (hPa)                                     | Wet Bulb (°C)                                                                                   | Humidex (°C)                             | Enthalpy (kJ/kg)                             |
|--------------------------------------|-----------|--------|-----------------------------|---------------------------------|--------------------------------------------------------------------|-----------------------------|--------------------------------------------|-------------------------------------------------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-----------------------------------------|---------------------------------------------|
| **Valid data**                       | 27.00     | 43.00  | 27.02                       | 15.60                           | 11.04                                                              | 0.21102                     | 0.27                                       | 15.29                                                       | 35.57                                                         | 18.54                                                                                            | 29.94                                   | 1124.19                                     |
| **Sensor read failure / invalid**    | nan       | nan    | nan                         | nan                             | nan                                                                 | nan                         | nan                                        | nan                                                         | nan                                                           | nan                                                                                              | nan                                     | nan                                         |
| **Formulas used**                    | T         | RH     | heatIndex = dht.computeHeatIndex(T, RH, false) | dewPoint = T - ((100 - RH) / 5.0) | absHumidity = 216.7 × (RH/100 × 6.112 × e^(17.62×T / (243.12+T)) / (273.15+T)) | specificHumidity = 0.622 × (RH/100) / (1 + 0.622 × (RH/100)) | mixingRatio = 622 × (RH/100) / (1000 - RH/100) | vaporPressure = RH/100 × 6.112 × e^(17.62×T / (243.12+T)) | satVaporPressure = 6.112 × e^(17.62×T / (243.12+T)) | wetBulb = complex empirical formula (see source code for full expression) | humidex = T + 0.5555 × (vaporPressure - 10.0) | enthalpy = 1.006×T + (2501 + 1.86×T) × RH/100 |

-- 

To process the data output from the Arduino Uno CH340G board into a visual format, the dht11_viewer.py script has been developed. This script functions as a real-time terminal interface that visualizes serial data from the board. It enhances readability using the colorama library for ANSI color formatting, and establishes communication via USB using the pyserial library.

To install the required libraries, use the following commands:

```bash
pip install colorama  # For ANSI color formatting
pip install pyserial  # For USB serial communication
```

Upon execution, the script imports all necessary dependencies and initializes terminal color settings. It then scans and lists available serial ports, verifying that the user-specified port (```e.g., /dev/tty.usbserial-1410```) is available. If the target port is not detected, the script exits gracefully with a descriptive error message.

Once connected, the script enters its main loop, continuously reading lines of data from the serial port. Each line is decoded and parsed into **12 expected floating-point values**, corresponding to: temperature, humidity, heat index, dew point, absolute humidity, specific humidity, mixing ratio, vapor pressure, saturation vapor pressure, wet bulb temperature, humidex, and enthalpy.

If a read or parse operation fails—due to invalid input or disconnection—the error is logged and displayed in red for clear visibility. Additionally, the script handles keyboard interrupts (```Ctrl+C```) to terminate the session safely and display a goodbye message along with the total uptime.

Example Output:
