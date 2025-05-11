# Advanced-Arduino-Weather-Station-Using-DHT11-and-Serial-Data-Logging

This project utilizes an **Arduino Uno CH340G development board** paired with a **DHT11** temperature and humidity sensor to create a compact yet capable environmental monitoring system. It measures **ambient temperature (°C)** and **relative humidity (%)**, and based on these, calculates a comprehensive set of derived atmospheric metrics including: Heat Index, Dew Point, Absolute Humidity, Specific Humidity, Mixing Ratio, Vapor Pressure, Saturation Vapor Pressure, Wet Bulb Temperature, Humidex, and Enthalpy.


The ```main.cpp``` sketch located in the ```/src``` directory of this repository consists of a C++ program that begins by importing the ```DHT.h``` library, as included in the ```platformio.ini``` config. After defining the sensor type and the corresponding data pin, the sketch initializes serial communication at a **9600 baud rate**. A short delay follows to allow the DHT11 sensor to stabilize before data collection begins. Within the ```loop()``` function, the program attempts to read temperature and humidity values from the sensor. If either value is **invalid (NaN)**, the system prints a row of **"nan"** values and waits one second before retrying. 

When valid data is received, the program proceeds to calculate multiple atmospheric parameters based on the raw sensor input. Before transmitting the results to the serial monitor, the program calls a function that blinks the onboard LED three times, visually signaling that the data was successfully retrieved from the DHT11 module. The calculated values are then output in comma-separated format at two-second intervals, providing a continuous stream of real-time environmental data.

### Example Output

Serial output:
```bash
27.00,43.00,27.02,15.60,11.04,0.21102,0.27,15.29,35.57,18.54,29.94,1124.19
nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
```  

Each row represents a full sensor readout and computed atmospheric metrics, output every 2 seconds:

| Description                          | Temp (°C) | RH (%) | Heat Index (°C) | Dew Point (°C) | Abs. Humidity (g/m³) | Spec. Humidity | Mix. Ratio (g/kg) | Vapor Pressure (hPa) | Sat. Vap. Pressure (hPa) | Wet Bulb (°C) | Humidex (°C) |
|--------------------------------------|-----------|--------|------------------|----------------|------------------------|----------------|--------------------|------------------------|----------------------------|----------------|----------------|
| **Valid data**                       | 27.00     | 43.00  | 27.02            | 15.60          | 11.04                  | 0.21102        | 0.27               | 15.29                  | 35.57                      | 18.54          | 29.94          |
| **Sensor read failure / invalid**    | nan       | nan    | nan              | nan            | nan                    | nan            | nan                | nan                    | nan                        | nan            | nan            |
| **Formulas used**                    | T         | RH     | HI = f(T, RH)    | DP ≈ T - ((100 - RH) / 5) | AH ≈ 216.7 × VP / (T + 273.15) | SH ≈ 0.622 × VP / (P - VP) | MR ≈ 0.622 × VP / (P - VP) | VP ≈ RH × SVP / 100 | SVP ≈ 6.11 × 10^(7.5 × T / (237.3 + T)) | WB ≈ empirical(T, RH) | Humidex ≈ T + 0.5555 × (VP - 10) |
