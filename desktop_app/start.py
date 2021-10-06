from argparse import ArgumentParser
from data_sources import InputSource, SourceHook
from display import Display, DisplayController
from serial.tools import list_ports
import serial, time, sys, platform

def serial_connection(serial_port, serial_baud_rate):
    
    # -- Detect Arduino Connection
    available_ports = list(list_ports.comports())

    for port in available_ports:
        if "Arduino" in port.description:

            if platform.system() == 'Windows':
                serial_port = port.name
            elif platform.system() == 'Darwin':
                serial_port = '/dev/' + port.name
            
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
        raise ConnectionError('Failed to connect to Arduino Device.')


def main(args):

    # -- Instantiate Display Window
    display = Display()

    # -- Instantiate Plotting Backend
    display_controller = DisplayController(display)

    if not args.no_serial:
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

        source_hook = SourceHook(arduino_obj, display_controller)
        source_hook.start_read_loop()
    else:
        user_input_source = InputSource()
        source_hook = SourceHook(user_input_source, display_controller)
        source_hook.start_read_loop()
        user_input_source.read_loop()

    # -- Start Display
    display_controller.start_display()


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--no-serial", action="store_true", default=False)
    args = arg_parser.parse_args()
    main(args)
