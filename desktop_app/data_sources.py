from abc import abstractmethod
from display import DisplayController
from threading import Timer
from typing import List


class Source():

    @property
    def in_waiting(self) -> int:
        return 0

    @abstractmethod
    def readline(self) -> bytes:
        pass


class InputSource(Source):

    def __init__(self, read_frequency: float = 10):
        self.data = []  # type: list[bytes]
        self.read_frequency = read_frequency

    @property
    def in_waiting(self) -> int:
        return len(self.data)

    def readline(self) -> bytes:
        first = self.data[0]
        self.data = self.data[1:]
        return first

    def put_manual_data(self):
        in_data = input().encode()
        self.data.append(in_data)

    def put_data(self, data: bytes):
        self.data.append(data)

    def start_read_loop(self):
        self.redraw_timer = Timer(1 / self.read_frequency, self.read_loop)
        self.redraw_timer.daemon = True  # Kill the timer when the program exits
        self.redraw_timer.start()

    def read_loop(self):
        self.put_manual_data()
        self.start_read_loop()


class SourceHook():

    def __init__(self, source: Source, display_controller: DisplayController, read_frequency: float = 10):
        self.source = source
        self.display_controller = display_controller
        self.read_frequency = read_frequency
        self.retry_timer = None

    def try_read(self):
        lines = []
        while self.source.in_waiting > 0:
            lines.append(self.source.readline().decode())
        for line in lines:
            analyte, datapoint = line.split(' ')
            datapoint = float(datapoint)
            self.display_controller.accept_data(analyte, datapoint)

    def start_read_loop(self):
        self.retry_timer = Timer(1 / self.read_frequency, self.read_loop)
        self.retry_timer.daemon = True  # Kill the timer when the program exits
        self.retry_timer.start()

    def read_loop(self):
        self.try_read()
        self.start_read_loop()
