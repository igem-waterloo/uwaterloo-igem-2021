from display import Display, DisplayController
from serial.tools import list_ports
import serial, time, sys

def serial_connection(serial_port, serial_baud_rate):
    
    # -- Detect Arduino Connection
    available_ports = list(list_ports.comports())

    for port in available_ports:
        if "Arduino" in port.description:
            serial_port = port.name

    if len(available_ports) == 0 or serial_port == '':
        raise ConnectionError('Arduino Device Not Connected.')

    # -- Establish Connection
    print('Trying to connect to: ' + str(serial_port) + ' at ' + str(serial_baud_rate) + ' BAUD.')
    try:
        serial_obj = serial.Serial(serial_port, serial_baud_rate, timeout=4)
        print('Connected to ' + str(serial_port) + ' at ' + str(serial_baud_rate) + ' BAUD.')
        return serial_obj

    except:
        print("Failed to connect with " + str(serial_port) + ' at ' + str(serial_baud_rate) + ' BAUD.')
        return ''


if __name__ =='__main__':

    # -- Serial Port Properties 
    port_name = ''
    baud_rate = 115200
    arduino_obj = ''
    connection_timeout = False

    t_initial = time.time()
    while arduino_obj == '':
        arduino_obj = serial_connection(port_name, baud_rate)
        if time.time() - t_initial > 10:
            connection_timeout = True
            break

    # -- Connection Failure by Timeout
    if connection_timeout:
        sys.exit('Connection Failure (Timeout)')

    # -- Instantiate Display Window
    display = Display()

    # -- Instantiate Plotting Backend
    display_controller = DisplayController(display)

    # -- Start Display
    Display.start_display()
