import time
from datetime import datetime
import serial
from colorama import Fore, Style, init
import serial.tools.list_ports

init(autoreset=True)

def choose_serial_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print(Fore.RED + "No serial ports found." + Style.RESET_ALL)
        exit(1)
    print(Fore.CYAN + "Available serial ports:" + Style.RESET_ALL)
    for i, port in enumerate(ports):
        print(Fore.YELLOW + f"  {i + 1}: {port.device} ({port.description})" + Style.RESET_ALL)
    while True:
        try:
            idx = int(input(Fore.CYAN + f"Select port [1-{len(ports)}] (default 1): " + Style.RESET_ALL) or "1")
            if 1 <= idx <= len(ports):
                return ports[idx - 1].device
        except Exception:
            pass
        print(Fore.RED + "Invalid selection. Try again." + Style.RESET_ALL)

def choose_baudrate(default=9600):
    val = input(Fore.CYAN + f"Enter baud rate (default {default}): " + Style.RESET_ALL)
    try:
        return int(val) if val else default
    except ValueError:
        print(Fore.RED + "Invalid baud rate, using default." + Style.RESET_ALL)
        return default

def print_instructions():
    print(Fore.MAGENTA + "╔" + "═" * 54 + "╗" + Style.RESET_ALL)
    print(Fore.MAGENTA + "║  Press Ctrl+C at any time to exit the program.       ║" + Style.RESET_ALL)
    print(Fore.MAGENTA + "╚" + "═" * 54 + "╝" + Style.RESET_ALL)

port = choose_serial_port()
baudrate = choose_baudrate()

ser = serial.Serial(port, baudrate, timeout=1)

def print_border():
    print(Fore.BLUE + "╔" + "═" * 54 + "╗" + Style.RESET_ALL)

def print_footer():
    print(Fore.BLUE + "╚" + "═" * 54 + "╝" + Style.RESET_ALL)

def print_log(msg, color=Fore.WHITE):
    now = datetime.now().strftime("%H:%M:%S")
    print(color + f"[{now}] {msg}" + Style.RESET_ALL)

spinner = ['|', '/', '-', '\\']
spin_idx = 0

last_error = None
log_history = []  # Store log entries (timestamp, message, color)

def add_log(msg, color=Fore.WHITE):
    now = datetime.now().strftime("%H:%M:%S")
    log_history.append((now, msg, color))
    # Keep only last 6 logs
    if len(log_history) > 6:
        log_history.pop(0)

def print_log_section():
    print(Fore.YELLOW + "║" + " " * 52 + Style.RESET_ALL)
    print(Fore.YELLOW + "║" + Style.BRIGHT + "   Log & Status:" + Style.RESET_ALL)
    for t, msg, color in log_history:
        log_line = f"[{t}] {msg}"
        print(Fore.YELLOW + "║ " + color + f"{log_line:<50}" + Style.RESET_ALL)
    # Fill remaining lines for consistent height
    for _ in range(6 - len(log_history)):
        print(Fore.YELLOW + "║" + " " * 52 + Style.RESET_ALL)
    print(Fore.YELLOW + "║" + " " * 52 + Style.RESET_ALL)

try:
    print_instructions()
    time.sleep(2)
    while True:
        # Show waiting animation
        add_log(f"Waiting for data {spinner[spin_idx % len(spinner)]}", Fore.CYAN)
        print(Fore.CYAN + f"\rWaiting for data {spinner[spin_idx % len(spinner)]}" + Style.RESET_ALL, end="")
        spin_idx += 1

        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
        except Exception as e:
            line = ''
            current_error = f"Serial read error: {e}"
            add_log(current_error, Fore.RED)
        else:
            current_error = None

        if line:
            add_log("Data received, parsing...", Fore.GREEN)
            try:
                temp, hum, heat, dew, abs_h, spec_h, mix, vp, svp, wb, humidex, enth = map(float, line.split(','))
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("\033c", end="")  # Clear screen

                print_border()
                print(Fore.BLUE + "║" + Style.BRIGHT + Fore.WHITE + "         Arduino Weather Station Live Feed            " + Style.RESET_ALL + Fore.BLUE + "║" + Style.RESET_ALL)
                print(Fore.BLUE + f"║   Latest update at {now}               ║" + Style.RESET_ALL)
                
                uptime = time.time() - ser.open_time if hasattr(ser, 'open_time') else None
                if uptime is None:
                    ser.open_time = time.time()
                    uptime = 0
                else:
                    uptime = time.time() - ser.open_time
                uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
                print(Fore.BLUE + f"║   Uptime: {uptime_str}" + Style.RESET_ALL)

                print_border()
                label_width = 22
                value_width = 8

                temp_approx = "±2.00"
                hum_approx = "±5.00"

                print(Fore.GREEN + f"║ {'Temp (°C):':<{label_width}} {temp:>{value_width}.2f}  (approx {temp_approx})" + Style.RESET_ALL)
                print(Fore.GREEN + f"║ {'Humidity (%):':<{label_width}} {hum:>{value_width}.2f}  (approx {hum_approx})" + Style.RESET_ALL)
                print(Fore.GREEN + f"║ {'Heat Index (°C):':<{label_width}} {heat:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.GREEN + f"║ {'Humidex:':<{label_width}} {humidex:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.GREEN + f"║ {'Dew Point (°C):':<{label_width}} {dew:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.GREEN + f"║ {'Wet Bulb Temp (°C):':<{label_width}} {wb:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.GREEN + f"║ {'Enthalpy (kJ/kg):':<{label_width}} {enth:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.GREEN + "║" + " " * 52 + Style.RESET_ALL)

                print(Fore.MAGENTA + f"║ {'Abs Humidity (g/m³):':<{label_width}} {abs_h:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.MAGENTA + f"║ {'Specific Humidity:':<{label_width}} {spec_h:>{value_width}.5f}" + Style.RESET_ALL)
                print(Fore.MAGENTA + f"║ {'Mixing Ratio (g/kg):':<{label_width}} {mix:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.MAGENTA + "║" + " " * 52 + Style.RESET_ALL)

                print(Fore.CYAN + f"║ {'Vapor Pressure (hPa):':<{label_width}} {vp:>{value_width}.2f}" + Style.RESET_ALL)
                print(Fore.CYAN + f"║ {'Sat Vapor Press.:':<{label_width}} {svp:>{value_width}.2f}" + Style.RESET_ALL)
                print_footer()

                # Print log section under the table
                print_log_section()
                print_instructions()

                if last_error:
                    add_log("Operation back to normal. Previous error resolved.", Fore.GREEN)
                    last_error = None

                add_log("Measurement received and displayed.", Fore.CYAN)
                time.sleep(0.5)

            except Exception as e:
                current_error = f"Error parsing line: {line} ({e})"
                add_log(current_error, Fore.RED)

        if current_error:
            if last_error != current_error:
                add_log(current_error, Fore.RED)
                last_error = current_error
            time.sleep(1)
except KeyboardInterrupt:
    print("\n" + Fore.MAGENTA + "Exiting. Goodbye!" + Style.RESET_ALL)

    uptime = time.time() - ser.open_time if hasattr(ser, 'open_time') else None
    if uptime is None:
        ser.open_time = time.time()
        uptime = 0
    else:
        uptime = time.time() - ser.open_time
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
    print(Fore.YELLOW + f"Uptime: {uptime_str}" + Style.RESET_ALL)