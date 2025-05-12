/**
 * @file main2.cpp
 * @brief Arduino DHT11 Weather Station - Live Serial Monitor with Logging and Metrics
 *
 * This program reads temperature and humidity data from a DHT11 sensor,
 * calculates various meteorological metrics, and displays them in a formatted
 * serial output with a live log section. It also provides visual feedback via
 * an onboard LED and maintains a short log history for status and error messages.
 *
 * Features:
 * - Reads temperature and humidity from DHT11 sensor.
 * - Calculates and displays:
 *     - Heat Index
 *     - Dew Point
 *     - Absolute Humidity
 *     - Specific Humidity
 *     - Mixing Ratio
 *     - Vapor Pressure
 *     - Saturation Vapor Pressure
 *     - Wet Bulb Temperature
 *     - Humidex
 *     - Enthalpy
 * - Maintains a rolling log of recent events and errors.
 * - Displays uptime and repository information.
 * - Blinks onboard LED for status indication and error notification.
 * - Handles sensor errors gracefully with log and visual feedback.
 *
 * Hardware:
 * - DHT11 sensor connected to digital pin 2.
 * - Onboard LED connected to digital pin 13.
 *
 * Dependencies:
 * - DHT sensor library
 * - Arduino core libraries
 *
 * @author HexKernel
 * @see https://github.com/HexKernel/Arduino-DHT11-Weather-Station
 */
#include <DHT.h>
#include <math.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define LED_PIN 13

DHT dht(DHTPIN, DHTTYPE);

const int LOG_SIZE = 6;
String log_history[LOG_SIZE];
unsigned long log_times[LOG_SIZE];
int log_count = 0;

void add_log(const String& msg) {
  if (log_count < LOG_SIZE) {
    log_history[log_count] = msg;
    log_times[log_count] = millis();
    log_count++;
  } else {
    for (int i = 1; i < LOG_SIZE; ++i) {
      log_history[i - 1] = log_history[i];
      log_times[i - 1] = log_times[i];
    }
    log_history[LOG_SIZE - 1] = msg;
    log_times[LOG_SIZE - 1] = millis();
  }
}

void print_border() {
  Serial.println("+----------------------------------------------------+");
}

void print_footer() {
  Serial.println("+----------------------------------------------------+");
}

void print_instructions() {
    Serial.println("+----------------------------------------------------+");
    Serial.println("| HexKernel | GitHub Repository                      |");
    Serial.println("| github.com/HexKernel/Arduino-DHT11-Weather-Station |");
    Serial.println("+----------------------------------------------------+");
  }  

void print_log_section() {
  Serial.println("Log & Status:                                    ");
  for (int i = 0; i < log_count; ++i) {
    // Print the wait message without timestamp
    if (log_history[i] == "=== WAIT FOR 10 SECONDS FOR SCREEN TO REFRESH ===") {
      Serial.print("  ");
      Serial.println(log_history[i]);
    } else {
      unsigned long sec = log_times[i] / 1000;
      char buf[64];
      snprintf(buf, sizeof(buf), "[%02lu:%02lu:%02lu] %s", sec/3600, (sec/60)%60, sec%60, log_history[i].c_str());
      Serial.print("  ");
      Serial.println(buf);
    }
  }
  for (int i = log_count; i < LOG_SIZE; ++i) {
    Serial.println("                                                     ");
  }
  Serial.println("                                                     ");
}

void blinkLed(int times, int delayMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(delayMs);
    digitalWrite(LED_PIN, LOW);
    delay(delayMs);
  }
}

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN, OUTPUT);
  delay(2000);
  Serial.println("Temp,Humidity,HeatIdx,DewPt,AbsHum,SpecHum,MixR,VapPres,SatVapPres,WetBulb,Humidex,Enthalpy");
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Clear log buffer at the start of each cycle
  log_count = 0;

  add_log("Measurement received from DHT11.");

  if (isnan(temp) || isnan(hum)) {
    add_log("Sensor error: nan values.");
    add_log("=== WAIT FOR 10 SECONDS FOR SCREEN TO REFRESH ===");
    print_log_section();
    print_instructions();
    for (int i = 0; i < 8; ++i) {
      blinkLed(1, 625); // 8 blinks over 5 seconds
      delay(625);
    }
    delay(5000); // Complete the 10 second wait
    return;
  }

  add_log("Calculations for metrics done.");

  float heatIndex = dht.computeHeatIndex(temp, hum, false);
  float dewPoint = temp - ((100 - hum) / 5.0);
  float absHumidity = 216.7 * ((hum / 100.0) * 6.112 * exp((17.62 * temp) / (243.12 + temp)) / (273.15 + temp));
  float specificHumidity = (0.622 * (hum / 100.0)) / (1 + (0.622 * (hum / 100.0)));
  float mixingRatio = (622 * (hum / 100.0)) / (1000 - (hum / 100.0));
  float vaporPressure = hum / 100.0 * 6.112 * exp((17.62 * temp) / (243.12 + temp));
  float satVaporPressure = 6.112 * exp((17.62 * temp) / (243.12 + temp));
  float wetBulb = temp * atan(0.151977 * sqrt(hum + 8.313659)) + atan(temp + hum) - atan(hum - 1.676331) + 0.00391838 * pow(hum, 1.5) * atan(0.023101 * hum) - 4.686035;
  float humidex = temp + 0.5555 * (vaporPressure - 10.0);
  float enthalpy = 1.006 * temp + (2501 + 1.86 * temp) * hum / 100.0;

  add_log("Parsing data to serial output.");
  blinkLed(3, 70);

  // Simulate clear screen
  for (int i = 0; i < 30; ++i) Serial.println();

  unsigned long uptime = millis() / 1000;
  char uptime_str[16];
  snprintf(uptime_str, sizeof(uptime_str), "%02lu:%02lu:%02lu", uptime/3600, (uptime/60)%60, uptime%60);

  print_border();
  Serial.println("|         Arduino Weather Station Live Feed          |");
  Serial.print("|         Uptime: "); Serial.print(uptime_str); Serial.println("                           |");
  print_border();

  // Remove ending | for metric section
  Serial.print("  Temp (C):           "); Serial.print(temp, 2); Serial.println("  (approx +/-2.00)");
  Serial.print("  Humidity (%):       "); Serial.print(hum, 2); Serial.println("  (approx +/-5.00)");
  Serial.print("  Heat Index (C):     "); Serial.print(heatIndex, 2); Serial.println();
  Serial.print("  Humidex:            "); Serial.print(humidex, 2); Serial.println();
  Serial.print("  Dew Point (C):      "); Serial.print(dewPoint, 2); Serial.println();
  Serial.print("  Wet Bulb Temp (C):  "); Serial.print(wetBulb, 2); Serial.println();
  Serial.print("  Enthalpy (kJ/kg):   "); Serial.print(enthalpy, 2); Serial.println();
  Serial.println();
  Serial.print("  Abs Humidity (g/m3):"); Serial.print(absHumidity, 2); Serial.println();
  Serial.print("  Specific Humidity:  "); Serial.print(specificHumidity, 5); Serial.println();
  Serial.print("  Mixing Ratio (g/kg):"); Serial.print(mixingRatio, 2); Serial.println();
  Serial.println();
  Serial.print("  Vapor Pressure (hPa):"); Serial.print(vaporPressure, 2); Serial.println();
  Serial.print("  Sat Vapor Press.:   "); Serial.print(satVaporPressure, 2); Serial.println();
  print_border();

  add_log("Successful display to serial monitor.");
  add_log("=== WAIT FOR 10 SECONDS FOR SCREEN TO REFRESH ===");

  print_log_section();
  print_instructions();

  // Blink 8 times during the wait (10 seconds total)
  for (int i = 0; i < 8; ++i) {
    blinkLed(1, 625);
    delay(625);
  }
}
